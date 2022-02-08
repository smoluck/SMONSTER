#perl
#ver 2.02
#author : Seneca Menard

#This script's been completely rewritten so that it works regardless of workplanes, item transforms, multiple item selected, etc, and now doesn't have any accidental roll of the perfect circle because the algo was finally done for real this time and wasn't a quick hack.

#(2-9-12 bugfix) : noticed my selection count safety check was assuming you'd always have verts selected.  it's now updated to know you can have verts or polys selected and now knows how many of each you have to have selected in order for the script to start working on that layer.
#(2-10-12 bugfix) : turning off symmetry, moving verts, and then turning it back on.  should theoretically keep everything symmetrical.

my $pi=3.1415926535897932384626433832795;
my @fgLayers = lxq("query layerservice layers ? fg");
my @fgLayerIDs;
my @originPos2D = (0,0);
my $selectType;
my $selMode;
my %layerElemList;

#turn off symmetry
my $symmAxis = lxq("select.symmetryState ?");
if ($symmAxis ne "none"){	lx("select.symmetryState none");	}

if		( lxq( "select.typeFrom {vertex;edge;polygon;item} ?" ) )	{	$selectType = "vertex";		$selMode = "verts";	}
elsif	( lxq( "select.typeFrom {edge;polygon;item;vertex} ?" ) )	{	$selectType = "edge";		$selMode = "edges";	}
elsif	( lxq( "select.typeFrom {polygon;item;vertex;edge} ?" ) )	{	$selectType = "polygon";	$selMode = "polys";	}
else																{	die("\\\\n.\\\\n[---------------------------------------------You're not in vert, edge, or polygon mode.--------------------------------------------]\\\\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \\\\n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\\\\n.\\\\n");}

#build per-layer elem list
foreach my $layer (@fgLayers){
	my $layerName = lxq("query layerservice layer.name ? $layer");
	@{$layerElemList{$layer}} = lxq("query layerservice $selMode ? selected");
}

#run script on each layer.
foreach my $fgLayer (@fgLayers){
	my $mainlayer = $fgLayer;
	my $mainlayerID = lxq("query layerservice layer.id ? $mainlayer");
	push(@fgLayerIDs,$mainlayerID);
	my $selTypeSafetyCheckCount = 0;

	if ($selectType eq "vertex"){
		my $vertList;
		$vertList .= ",".$_ for @{$layerElemList{$fgLayer}};
		$vertList .= ",".${$layerElemList{$fgLayer}}[0];
		$vertList =~ s/$\,//;
		@vertRowList = ($vertList);
		$selTypeSafetyCheckCount = 2;
	}

	elsif ($selectType eq "edge"){
		sortRowStartup(edgesSelected,@{$layerElemList{$fgLayer}});
		$selTypeSafetyCheckCount = 2;
	}

	elsif ($selectType eq "polygon"){
		my @borderEdges = returnBorderEdges(\@{$layerElemList{$fgLayer}});
		sortRowStartup(dontFormat,@borderEdges);
		$selTypeSafetyCheckCount = 0;
	}

	if (@{$layerElemList{$fgLayer}} > $selTypeSafetyCheckCount){
		lx("select.subItem {$mainlayerID} set mesh;camera;light;backdrop;groupLocator;replicator;locator;deform;locdeform;chanModify;chanEffect 0 0");
		perfectCircle();
	}else{
		lxout("Skipping layer ($fgLayer) because it has less than 3 verts selected");
	}
}

#restore original fglayers and selection
lx("select.subItem {$_} add mesh;camera;light;backdrop;groupLocator;replicator;locator;deform;locdeform;chanModify;chanEffect 0 0") for @fgLayerIDs;
lx("select.type $selectType");
if ($selectType eq "edge"){
	foreach my $layer (@fgLayers){
		foreach my $edge (@{$layerElemList{$layer}}){
			my @verts = split (/[^0-9]/, $edge);
			lx("select.element {$layer} edge add {$verts[1]} {$verts[2]}");
		}
	}
}else{
	foreach my $layer (@fgLayers){
		lx("select.element {$layer} {$selectType} add {$_}") for @{$layerElemList{$layer}};
	}
}


#turn symmetry back on.
if ($symmAxis ne "none"){	lx("select.symmetryState $symmAxis");	}









#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#PERFECT CIRCLE SUB
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub perfectCircle{
	foreach my $vertRow (@vertRowList){
		my @verts = split (/[^0-9]/, $vertRow);
		my @vertsReorder = @verts;
		my %posTable = ();
		my %unitVecTable = ();
		my %unitVecTable2d = ();
		my %unitVecTableFake2d = ();
		my $greatestDP;
		my $mostImportantVert;
		my @mostImportantEdgeVec;

		my $constHalfRadian = (360/$#verts) * ($pi/180) * -.5;
		my @matrixAngleRotateZ_edgeOffset = (
			[cos($constHalfRadian), -sin($constHalfRadian), 0, 0],
			[sin($constHalfRadian), cos($constHalfRadian), 0, 0],
			[0, 0, 1, 0],
			[0, 0, 0, 1]
		);


		#--------------------------------------------
		#DETERMINE TRANSFORM MATRIX
		#--------------------------------------------
		my @avgVertNormal = (0,0,0);
		my @avgPos = (0,0,0);
		my @vertsPosList;
		for (my $i=0; $i<$#verts; $i++){
			my @pos = lxq("query layerservice vert.pos ? $verts[$i]");
			@avgPos = arrMath(@pos,@avgPos,add);
			push(@vertsPosList,\@pos);
		}
		@avgPos = arrMath(@avgPos,$#verts,$#verts,$#verts,div);

		for (my $i=0; $i<$#verts; $i++){
			my @vec1 = unitVector(${$vertsPosList[$i-1]}[0] - ${$vertsPosList[$i]}[0] , ${$vertsPosList[$i-1]}[1] - ${$vertsPosList[$i]}[1] , ${$vertsPosList[$i-1]}[2] - ${$vertsPosList[$i]}[2]);
			my @vec2 = unitVector(${$vertsPosList[$i-2]}[0] - ${$vertsPosList[$i-1]}[0] , ${$vertsPosList[$i-2]}[1] - ${$vertsPosList[$i-1]}[1] , ${$vertsPosList[$i-2]}[2] - ${$vertsPosList[$i-1]}[2]);
			my @cp = crossProduct(\@vec1,\@vec2);
			@avgVertNormal = arrMath(@avgVertNormal,@cp,add);
		}
		@avgVertNormal = unitVector(@avgVertNormal);

		my @vecX = unitVector(arrMath(lxq("query layerservice vert.pos ? $verts[0]"),@avgPos,subt));
		my @vecY = crossProduct(\@avgVertNormal,\@vecX);
		@vecX = crossProduct(\@vecY,\@avgVertNormal);

		####if ($debug eq "a"){
		####	lxout("avgPos = @avgPos");
		####	lxout("vecX = @vecX");
		####	lxout("vecY = @vecY");
		####	lxout("avgVertNormal = @avgVertNormal");
		####
		####	my @locX = arrMath(@avgPos,@vecX,add);
		####	my @locY = arrMath(@avgPos,@vecY,add);
		####	my @locZ = arrMath(@avgPos,@avgVertNormal,add);
		####	createTextLoc(@avgPos,"cen",.001);
		####	createTextLoc(@locX,"X",.001);
		####	createTextLoc(@locY,"Y",.001);
		####	createTextLoc(@locZ,"Z",.001);
		####	return;
		####}

		my @matrix = (
			[1,0,0,-$avgPos[0]],
			[0,1,0,-$avgPos[1]],
			[0,0,1,-$avgPos[2]],
			[0,0,0,1]
		);

		my @rotMatrix = (
			[@vecX,0],
			[@vecY,0],
			[@avgVertNormal,0],
			[0,0,0,1]
		);

		@matrix = mtxMult(\@rotMatrix,\@matrix);
		my @invMatrix = inverseMatrix(\@matrix);


		#--------------------------------------------
		#STORE OUT LOCAL SPACE VERT POSITIONS.
		#--------------------------------------------
		foreach my $vert (@verts){
			my @pos = lxq("query layerservice vert.pos ? $vert");
			@pos = vec_mtxMult(\@matrix,\@pos);
			@{$posTable{$vert}} = @pos;
			@{$unitVecTable{$vert}} = unitVector(@pos);
			@{$unitVecTable2d{$vert}} = (@{$unitVecTable{$vert}}[0],@{$unitVecTable{$vert}}[1]);
			@{$unitVecTableFake2d{$vert}} = unitVector(@{$unitVecTable{$vert}}[0],@{$unitVecTable{$vert}}[1],0);
		}


		#--------------------------------------------
		#REVERSE VERTROW IF GOING WRONG DIR
		#--------------------------------------------
		my $angleSum = 0;
		for (my $i=0; $i<$#vertsReorder; $i++){
			my $angle = getAngleFrom3Pos2D(\@{$unitVecTable2d{$vertsReorder[$i]}},\@originPos2D,\@{$unitVecTable2d{$vertsReorder[$i+1]}});
			$angleSum += $angle;
		}
		if ($angleSum > 0){@vertsReorder = reverse(@vertsReorder);}



		#--------------------------------------------
		#DETERMINE BEST VERT BY VERT DPSUMS
		#--------------------------------------------
		for (my $i=0; $i<$#vertsReorder; $i++){
			shift(@vertsReorder);
			my $vert = shift(@vertsReorder);
			unshift(@vertsReorder,$vert);
			push(@vertsReorder,$vert);
			my $dpSum = 0;
			my $edgeDpSum = 0;
			my @edgeVec = (0,0,0);

			for (my $j=0; $j<$#vertsReorder; $j++){
				my $angle = (360/$#verts) * $j;
				my $radian = $angle * ($pi/180);
				my $halfRadian = $radian * .5;
				my @matrixAngleRotateZ = (
					[cos($radian), -sin($radian), 0, 0],
					[sin($radian), cos($radian), 0, 0],
					[0, 0, 1, 0],
					[0, 0, 0, 1]
				);

				my @rotatedVector = vec_mtxMult(\@matrixAngleRotateZ,\@{$unitVecTableFake2d{$vertsReorder[0]}});
				@edgeVec = arrMath(@{$unitVecTableFake2d{$vertsReorder[0]}},@{$unitVecTableFake2d{$vertsReorder[1]}},add);
				@edgeVec = arrMath(@edgeVec,.5,.5,.5,mult);
				@edgeVec = unitVector(@edgeVec);
				@edgeVec = vec_mtxMult(\@matrixAngleRotateZ_edgeOffset,\@edgeVec);
				my @rotatedEdgeVec = vec_mtxMult(\@matrixAngleRotateZ,\@edgeVec);

				####if ($i == $debug){
				####	my @tempPos = vec_mtxMult(\@invMatrix,\@rotatedEdgeVec);
				####	if ($j == 0){createTextLoc(@tempPos,$vertsReorder[$j],1);}
				####	else		{createTextLoc(@tempPos,$vertsReorder[$j],.001);}
				####
				####	my @tempPos1 = arrMath(@rotatedVector,.5,.5,.5,mult);
				####	@tempPos1 = vec_mtxMult(\@invMatrix,\@tempPos1);
				####	if ($j == 0){createTextLoc(@tempPos1,$vertsReorder[$j],1);}
				####	else		{createTextLoc(@tempPos1,$vertsReorder[$j],.001);}
				####}

				$dpSum += dotProduct(\@{$unitVecTableFake2d{$vertsReorder[$j]}},\@rotatedVector);
				$edgeDpSum += dotProduct(\@{$unitVecTableFake2d{$vertsReorder[$j]}},\@rotatedEdgeVec);
			}
			#if ($i == $debug){return;}

			if ($dpSum > $greatestDP){
				$greatestDP = $dpSum;
				$mostImportantVert = $vertsReorder[0];
				#lxout("$i mostImportantVert = $mostImportantVert");
			}
			if ($edgeDpSum > $greatestDP){
				$greatestDP = $edgeDpSum;
				$mostImportantVert = $vertsReorder[0] . "," . $vertsReorder[1];
				@mostImportantEdgeVec = @edgeVec;
				#lxout("$i mostImportantEdge = $mostImportantVert");
			}
		}

		#--------------------------------------------
		#REORDER VERTLIST SO IMPORTANT VERT IS FIRST.
		#--------------------------------------------
		pop(@vertsReorder);
		my @array1;
		my @array2;
		my $foundVert = 0;
		my $mostImportantVertCopy = $mostImportantVert;
		$mostImportantVertCopy =~ s/,.*//;
		for (my $i=0; $i<@vertsReorder; $i++){
			if ($vertsReorder[$i] == $mostImportantVertCopy)	{	$foundVert = 1;						}
			if ($foundVert == 0)								{	push(@array1,$vertsReorder[$i]);	}
			else												{	push(@array2,$vertsReorder[$i]);	}
		}
		@vertsReorder = (@array2,@array1);


		#--------------------------------------------
		#FIND RADIUS
		#--------------------------------------------
		my $radiusAverage;
		for (my $i=0; $i<@vertsReorder; $i++){$radiusAverage += distance($posTable{$vertsReorder[$i]},$posTable{$vertsReorder[$i-1]});}
		$radiusAverage = $radiusAverage / ($pi*2);


		#--------------------------------------------
		#NOW FINALLY MOVE VERTS
		#--------------------------------------------
		my @firstVertVec = arrMath(@{$unitVecTableFake2d{$vertsReorder[0]}},$radiusAverage,$radiusAverage,$radiusAverage,mult);
		for (my $i=0; $i<@vertsReorder; $i++){
			my $angle = (360/@vertsReorder) * $i;
			my $radian = $angle * ($pi/180);
			my @matrixAngleRotateZ = (
				[cos($radian), -sin($radian), 0, 0],
				[sin($radian), cos($radian), 0, 0],
				[0, 0, 1, 0],
				[0, 0, 0, 1]
			);

			my @pos;
			if ($mostImportantVert =~ /,/){
				@pos = arrMath(@mostImportantEdgeVec,$radiusAverage,$radiusAverage,$radiusAverage,mult);
				@pos = vec_mtxMult(\@matrixAngleRotateZ,\@pos);
			}else{
				@pos = vec_mtxMult(\@matrixAngleRotateZ,\@firstVertVec);
			}
			@pos = vec_mtxMult(\@invMatrix,\@pos);
			lx("vert.move vertIndex:$vertsReorder[$i] posX:$pos[0] posY:$pos[1] posZ:$pos[2]");
		}
	}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#DISTANCE subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @dist = distance(\@pos1,\@pos0);
sub distance{
	my $disp0 = $_[0][0] - $_[1][0];
	my $disp1 = $_[0][1] - $_[1][1];
	my $disp2 = $_[0][2] - $_[1][2];

	my $dist = sqrt(($disp0*$disp0)+($disp1*$disp1)+($disp2*$disp2));
	return $dist;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#DOT PRODUCT subroutine (ver 1.1)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my $dp = dotProduct(\@vector1,\@vector2);
sub dotProduct{
	return (	(${$_[0]}[0]*${$_[1]}[0])+(${$_[0]}[1]*${$_[1]}[1])+(${$_[0]}[2]*${$_[1]}[2])	);
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#GET ANGLE FROM THREE 2D POSITIONS (start,middle,end) (middle is the angle being measured) <modded to return correct value across the angle boundary>
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : getAngleFrom3Pos2D(\@start,\@middle,\@end);
sub getAngleFrom3Pos2D{
	my $pi=3.1415926535897932384626433832795;
	my @disp1 = unitVector2d(arrMath2D(@{$_[0]},@{$_[1]},subt));
	my @disp2 = unitVector2d(arrMath2D(@{$_[2]},@{$_[1]},subt));

	my $radian = atan2($disp1[0],$disp1[1]);
	my $angle = ($radian*180)/$pi;
	my $radian2 = atan2($disp2[0],$disp2[1]);
	my $angle2 = ($radian2*180)/$pi;

	if		(($angle2 > 90) && ($angle < -90)){	$angle += 360;	}
	elsif	(($angle > 90) && ($angle2 < -90)){	$angle2 += 360;	}

	my $finalAngle = $angle2 - $angle;
	if ($finalAngle < -180){$finalAngle += 180;}

	return $finalAngle;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#PERFORM MATH FROM ONE ARRAY TO ANOTHER 2D subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @disp = arrMath(@pos2,@pos1,subt);
sub arrMath2D{
	my @array1 = (@_[0],@_[1]);
	my @array2 = (@_[2],@_[3]);
	my $math = @_[4];

	my @newArray;
	if		($math eq "add")	{	@newArray = (@array1[0]+@array2[0],@array1[1]+@array2[1]);	}
	elsif	($math eq "subt")	{	@newArray = (@array1[0]-@array2[0],@array1[1]-@array2[1]);	}
	elsif	($math eq "mult")	{	@newArray = (@array1[0]*@array2[0],@array1[1]*@array2[1]);	}
	elsif	($math eq "div")	{	@newArray = (@array1[0]/@array2[0],@array1[1]/@array2[1]);	}
	return @newArray;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#UNIT VECTOR 2D
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @unitVector2d = unitVector2d(@vector);
sub unitVector2d{
	my $dist1 = sqrt((@_[0]*@_[0])+(@_[1]*@_[1]));
	@_ = ((@_[0]/$dist1),(@_[1]/$dist1));
	return @_;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#QUERY ITEM REFERENCE MODE MATRIX (4x4)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @itemRefMatrix = getItemXfrmMatrix();
#if you multiply a vert by this matrix, you'll get the vert pos you see in screenspace
sub getItemRefMatrix{
	my $itemRef = lxq("item.refSystem ?");
	if ($itemRef eq ""){
		my @matrix = (
			[1,0,0,0],
			[0,1,0,0],
			[0,0,1,0],
			[0,0,0,1]
		);
		return @matrix;
	}else{
		my @itemXfrmMatrix = getItemXfrmMatrix($itemRef);
		@itemXfrmMatrix = inverseMatrix(\@itemXfrmMatrix);

		return @itemXfrmMatrix;
	}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#GET ITEM XFRM MATRIX (of the item and all it's parents and pivots)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @itemXfrmMatrix = getItemXfrmMatrix($itemID);
#if you multiply the verts by it's matrix, it gives their world positions.
sub getItemXfrmMatrix{
	my ($id) = $_[0];

	my @matrix = (
		[1,0,0,0],
		[0,1,0,0],
		[0,0,1,0],
		[0,0,0,1]
	);

	while ($id ne ""){
		my @transformIDs = lxq("query sceneservice item.xfrmItems ? {$id}");
		my @pivotTransformIDs;
		my @pivotRotationIDs;

		#find any pivot move or pivot rotate transforms
		foreach my $transID (@transformIDs){
			my $name = lxq("query sceneservice item.name ? $transID");
			$name =~ s/\s\([0-9]+\)$//;
			if ($name eq "Pivot Position"){
				push(@pivotTransformIDs,$transID);
			}elsif ($name eq "Pivot Rotation"){
				push(@pivotRotationIDs,$transID);
			}
		}

		#go through transforms
		foreach my $transID (@transformIDs){
			my $name = lxq("query sceneservice item.name ? $transID");
			my $type = lxq("query sceneservice item.type ? $transID");
			my $channelCount = lxq("query sceneservice channel.n ?");

			#rotation
			if ($type eq "rotation"){
				my $rotX = lxq("item.channel rot.X {?} set {$transID}");
				my $rotY = lxq("item.channel rot.Y {?} set {$transID}");
				my $rotZ = lxq("item.channel rot.Z {?} set {$transID}");
				my $rotOrder = uc(lxq("item.channel order {?} set {$transID}")) . "s";
				my @rotMatrix = Eul_ToMatrix($rotX,$rotY,$rotZ,$rotOrder,"degrees");
				@rotMatrix = convert3x3M_4x4M(\@rotMatrix);
				@matrix = mtxMult(\@rotMatrix,\@matrix);
			}

			#translation
			elsif ($type eq "translation"){
				my $posX = lxq("item.channel pos.X {?} set {$transID}");
				my $posY = lxq("item.channel pos.Y {?} set {$transID}");
				my $posZ = lxq("item.channel pos.Z {?} set {$transID}");
				my @posMatrix = (
					[1,0,0,$posX],
					[0,1,0,$posY],
					[0,0,1,$posZ],
					[0,0,0,1]
				);
				@matrix = mtxMult(\@posMatrix,\@matrix);
			}

			#scale
			elsif ($type eq "scale"){
				my $sclX = lxq("item.channel scl.X {?} set {$transID}");
				my $sclY = lxq("item.channel scl.Y {?} set {$transID}");
				my $sclZ = lxq("item.channel scl.Z {?} set {$transID}");
				my @sclMatrix = (
					[$sclX,0,0,0],
					[0,$sclY,0,0],
					[0,0,$sclZ,0],
					[0,0,0,1]
				);
				@matrix = mtxMult(\@sclMatrix,\@matrix);
			}

			#transform
			elsif ($type eq "transform"){
				#transform : piv pos
				if ($name =~ /pivot position inverse/i){
					my $posX = lxq("item.channel pos.X {?} set {$pivotTransformIDs[0]}");
					my $posY = lxq("item.channel pos.Y {?} set {$pivotTransformIDs[0]}");
					my $posZ = lxq("item.channel pos.Z {?} set {$pivotTransformIDs[0]}");
					my @posMatrix = (
						[1,0,0,$posX],
						[0,1,0,$posY],
						[0,0,1,$posZ],
						[0,0,0,1]
					);
					@posMatrix = inverseMatrix(\@posMatrix);
					@matrix = mtxMult(\@posMatrix,\@matrix);
				}

				#transform : piv rot
				elsif ($name =~ /pivot rotation inverse/i){
					my $rotX = lxq("item.channel rot.X {?} set {$pivotRotationIDs[0]}");
					my $rotY = lxq("item.channel rot.Y {?} set {$pivotRotationIDs[0]}");
					my $rotZ = lxq("item.channel rot.Z {?} set {$pivotRotationIDs[0]}");
					my $rotOrder = uc(lxq("item.channel order {?} set {$pivotRotationIDs[0]}")) . "s";
					my @rotMatrix = Eul_ToMatrix($rotX,$rotY,$rotZ,$rotOrder,"degrees");
					@rotMatrix = convert3x3M_4x4M(\@rotMatrix);
					@rotMatrix = transposeRotMatrix(\@rotMatrix);
					@matrix = mtxMult(\@rotMatrix,\@matrix);
				}

				else{
					lxout("type is a transform, but not a PIVPOSINV or PIVROTINV! : $type");
				}
			}

			#other?!
			else{
				lxout("type is neither rotation or translation! : $type");
			}
		}
		$id = lxq("query sceneservice item.parent ? $id");
	}
	return @matrix;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CONVERT 3X3 MATRIX TO EULERS (in any rotation order)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @angles = Eul_FromMatrix(\@3x3matrix,"XYZs",degrees|radians);
# - the output will be radians unless the third argument is "degrees" in which case the sub will convert it to degrees for you.
# - returns XrotAmt, YrotAmt, ZrotAmt, rotOrder;
# - resulting matrix must be inversed or transposed for it to be correct in modo.
sub Eul_FromMatrix{
	my ($m, $order) = @_;
	my @ea = (0,0,0,0);
	my $orderBackup = $order;

	my $pi = 3.14159265358979323;
	my $FLT_EPSILON = 0.00000000000000000001;
	my $EulFrmS = 0;
	my $EulFrmR = 1;
	my $EulRepNo = 0;
	my $EulRepYes = 1;
	my $EulParEven = 0;
	my $EulParOdd = 1;
	my @EulSafe = (0,1,2,0);
	my @EulNext = (1,2,0,1);

	#convert order text to indice
	my %rotOrderSetup = (
		"XYZs" , 0,		"XYXs" , 2,		"XZYs" , 4,		"XZXs" , 6,
		"YZXs" , 8,		"YZYs" , 10,	"YXZs" , 12,	"YXYs" , 14,
		"ZXYs" , 16,	"ZXZs" , 18,	"ZYXs" , 20,	"ZYZs" , 22,
		"ZYXr" , 1,		"XYXr" , 3,		"YZXr" , 5,		"XZXr" , 7,
		"XZYr" , 9,		"YZYr" , 11,	"ZXYr" , 13,	"YXYr" , 15,
		"YXZr" , 17,	"ZXZr" , 19,	"XYZr" , 21,	"ZYZr" , 23
	);
	$order = $rotOrderSetup{$order};


	$o=$order&31;
	$f=$o&1;
	$o>>=1;
	$s=$o&1;
	$o>>=1;
	$n=$o&1;
	$o>>=1;
	$i=@EulSafe[$o&3];
	$j=@EulNext[$i+$n];
	$k=@EulNext[$i+1-$n];
	$h=$s?$k:$i;

	if ($s == $EulRepYes) {
		$sy = sqrt($$m[$i][$j]*$$m[$i][$j] + $$m[$i][$k]*$$m[$i][$k]);
		if ($sy > 16*$FLT_EPSILON) {
			$ea[0] = atan2($$m[$i][$j], $$m[$i][$k]);
			$ea[1] = atan2($sy, $$m[$i][$i]);
			$ea[2] = atan2($$m[$j][$i], -$$m[$k][$i]);
		}else{
			$ea[0] = atan2(-$$m[$j][$k], $$m[$j][$j]);
			$ea[1] = atan2($sy, $$m[$i][$i]);
			$ea[2] = 0;
		}
	}else{
		$cy = sqrt($$m[$i][$i]*$$m[$i][$i] + $$m[$j][$i]*$$m[$j][$i]);
		if ($cy > 16*$FLT_EPSILON) {
			$ea[0] = atan2($$m[$k][$j], $$m[$k][$k]);
			$ea[1] = atan2(-$$m[$k][$i], $cy);
			$ea[2] = atan2($$m[$j][$i], $$m[$i][$i]);
		}else{
			$ea[0] = atan2(-$$m[$j][$k], $$m[$j][$j]);
			$ea[1] = atan2(-$$m[$k][$i], $cy);
			$ea[2] = 0;
		}
	}
	if ($n == $EulParOdd)	{	$ea[0] = -$ea[0]; $ea[1] = -$ea[1]; $ea[2] = -$ea[2];	}
	if ($f == $EulFrmR)		{	$t = $ea[0]; $ea[0] = $ea[2]; $ea[2] = $t;				}
	$ea[3] = $order;

	#convert radians to degrees if user wanted
	if ($_[2] eq "degrees"){
		$ea[0] *= 180/$pi;
		$ea[1] *= 180/$pi;
		$ea[2] *= 180/$pi;
	}

	#convert rot order back to lowercase text
	$ea[3] = lc($orderBackup);
	$ea[3] =~ s/[sr]//;

	#reorder rotations so they're always in X, Y, Z display order.
	my @eularOrder;
	$eularOrder[0] = substr($ea[3], 0, 1);
	$eularOrder[1] = substr($ea[3], 1, 1);
	$eularOrder[2] = substr($ea[3], 2, 1);
	my @eaBackup = @ea;
	for (my $i=0; $i<@eularOrder; $i++){
		if ($eularOrder[$i] =~ /x/i){$ea[0] = $eaBackup[$i];}
		if ($eularOrder[$i] =~ /y/i){$ea[1] = $eaBackup[$i];}
		if ($eularOrder[$i] =~ /z/i){$ea[2] = $eaBackup[$i];}
	}

	return @ea;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CONVERT EULER ANGLES TO (3 X 3) MATRIX (in any rotation order)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @3x3Matrix = Eul_ToMatrix($xRot,$yRot,$zRot,"ZXYs",degrees|radians);
# - the angles must be radians unless the fifth argument is "degrees" in which case the sub will convert it to radians for you.
# - must insert the X,Y,Z rotation values in the listed order.  the script will rearrange them internally.
# - as for the rotation order cvar, the last character is "s" or "r".  Here's what they mean:
#	"s" : "static axes"		: use this as default
#	"r" : "rotating axes"	: for body rotation axes?
# - resulting matrix must be inversed or transposed for it to be correct in modo.
sub Eul_ToMatrix{
	my $pi = 3.14159265358979323;
	my $FLT_EPSILON = 0.00000000000000000001;
	my $EulFrmS = 0;
	my $EulFrmR = 1;
	my $EulRepNo = 0;
	my $EulRepYes = 1;
	my $EulParEven = 0;
	my $EulParOdd = 1;
	my @EulSafe = (0,1,2,0);
	my @EulNext = (1,2,0,1);
	my @ea = @_;
	my @m = ([0,0,0],[0,0,0],[0,0,0]);

	#convert degrees to radians if user specified
	if ($_[4] eq "degrees"){
		$ea[0] *= $pi/180;
		$ea[1] *= $pi/180;
		$ea[2] *= $pi/180;
	}

	#reorder rotation value args to match same order as rotation order.
	my $rotOrderCopy = $ea[3];
	$rotOrderCopy =~ s/X/$ea[0],/g;
	$rotOrderCopy =~ s/Y/$ea[1],/g;
	$rotOrderCopy =~ s/Z/$ea[2],/g;
	my @eaCopy = split(/,/, $rotOrderCopy);
	$ea[0] = $eaCopy[0];
	$ea[1] = $eaCopy[1];
	$ea[2] = $eaCopy[2];

	my %rotOrderSetup = (
		"XYZs" , 0,		"XYXs" , 2,		"XZYs" , 4,		"XZXs" , 6,
		"YZXs" , 8,		"YZYs" , 10,	"YXZs" , 12,	"YXYs" , 14,
		"ZXYs" , 16,	"ZXZs" , 18,	"ZYXs" , 20,	"ZYZs" , 22,
		"ZYXr" , 1,		"XYXr" , 3,		"YZXr" , 5,		"XZXr" , 7,
		"XZYr" , 9,		"YZYr" , 11,	"ZXYr" , 13,	"YXYr" , 15,
		"YXZr" , 17,	"ZXZr" , 19,	"XYZr" , 21,	"ZYZr" , 23
	);
	$ea[3] = $rotOrderSetup{$ea[3]};

	#initial code
	$o=$ea[3]&31;
	$f=$o&1;
	$o>>=1;
	$s=$o&1;
	$o>>=1;
	$n=$o&1;
	$o>>=1;
	$i=$EulSafe[$o&3];
	$j=$EulNext[$i+$n];
	$k=$EulNext[$i+1-$n];
	$h=$s?$k:$i;

	if ($f == $EulFrmR)		{	$t = $ea[0]; $ea[0] = $ea[2]; $ea[2] = $t;				}
	if ($n == $EulParOdd)	{	$ea[0] = -$ea[0]; $ea[1] = -$ea[1]; $ea[2] = -$ea[2];	}
	$ti = $ea[0];
	$tj = $ea[1];
	$th = $ea[2];

	$ci = cos($ti); $cj = cos($tj); $ch = cos($th);
	$si = sin($ti); $sj = sin($tj); $sh = sin($th);
	$cc = $ci*$ch; $cs = $ci*$sh; $sc = $si*$ch; $ss = $si*$sh;

	if ($s == $EulRepYes) {
		$m[$i][$i] = $cj;		$m[$i][$j] =  $sj*$si;			$m[$i][$k] =  $sj*$ci;
		$m[$j][$i] = $sj*$sh;	$m[$j][$j] = -$cj*$ss+$cc;		$m[$j][$k] = -$cj*$cs-$sc;
		$m[$k][$i] = -$sj*$ch;	$m[$k][$j] =  $cj*$sc+$cs;		$m[$k][$k] =  $cj*$cc-$ss;
	}else{
		$m[$i][$i] = $cj*$ch;	$m[$i][$j] = $sj*$sc-$cs;		$m[$i][$k] = $sj*$cc+$ss;
		$m[$j][$i] = $cj*$sh;	$m[$j][$j] = $sj*$ss+$cc;		$m[$j][$k] = $sj*$cs-$sc;
		$m[$k][$i] = -$sj;		$m[$k][$j] = $cj*$si;			$m[$k][$k] = $cj*$ci;
    }

    return @m;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CONVERT 3X3 MATRIX TO 4X4 MATRIX
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#my @4x4Matrix = convert3x3M_4x4M(\@3x3Matrix);
sub convert3x3M_4x4M{
	my ($m) = $_[0];
	my @matrix = (
		[$$m[0][0],$$m[0][1],$$m[0][2],0],
		[$$m[1][0],$$m[1][1],$$m[1][2],0],
		[$$m[2][0],$$m[2][1],$$m[2][2],0],
		[0,0,0,1]
	);

	return @matrix;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#4 X 4 ROTATION MATRIX FLIP (only works on rotation-only matrices though)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#usage @matrix = transposeRotMatrix(\@matrix);
sub transposeRotMatrix{
	my @matrix = (
		[ @{$_[0][0]}[0],@{$_[0][1]}[0],@{$_[0][2]}[0],@{$_[0][0]}[3] ],	#[a00,a10,a20,a03],
		[ @{$_[0][0]}[1],@{$_[0][1]}[1],@{$_[0][2]}[1],@{$_[0][1]}[3] ],	#[a01,a11,a21,a13],
		[ @{$_[0][0]}[2],@{$_[0][1]}[2],@{$_[0][2]}[2],@{$_[0][2]}[3] ],	#[a02,a12,a22,a23],
		[ @{$_[0][3]}[0],@{$_[0][3]}[1],@{$_[0][3]}[2],@{$_[0][3]}[3] ]		#[a30,a31,a32,a33],
	);
	return @matrix;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CREATE TEXT LOCATOR ITEM
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : createTextLoc($x,$y,$z,$text,$locSize);
sub createTextLoc{
	lx("item.create locator");
	my @locatorSelection = lxq("query sceneservice selection ? locator");
	lx("transform.channel pos.X {$_[0]}");
	lx("transform.channel pos.Y {$_[1]}");
	lx("transform.channel pos.Z {$_[2]}");

	lx("!!item.name item:{$locatorSelection[-1]} name:{$_[3]}");
	lx("!!item.help add label {$_[3]}");
	lx("!!item.channel size {$_[4]} set {$locatorSelection[-1]}");
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CREATE A CUBE AT THE SPECIFIED PLACE/SCALE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub createCube{
	if (@_[3] eq undef){@_[3] = 5;}
	lx("tool.set prim.cube on");
	lx("tool.reset");
	lx("tool.setAttr prim.cube cenX {@_[0]}");
	lx("tool.setAttr prim.cube cenY {@_[1]}");
	lx("tool.setAttr prim.cube cenZ {@_[2]}");
	lx("tool.setAttr prim.cube sizeX {@_[3]}");
	lx("tool.setAttr prim.cube sizeY {@_[3]}");
	lx("tool.setAttr prim.cube sizeZ {@_[3]}");
	lx("tool.doApply");
	lx("tool.set prim.cube off");
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CREATE AXIS WEDGE FROM MATRIX (works on 3x3 and 4x4)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : createAxisWedge(\@matrix);
sub createAxisWedge{
	my $matrix = $_[0];
	my @offset = (0,0,0);
	if (@$matrix == 4){	@offset = ($$matrix[0][3] , $$matrix[1][3] , $$matrix[2][3]);	}
	my @pos1 = ($$matrix[0][0]+$offset[0] , $$matrix[0][1]+$offset[1] , $$matrix[0][2]+$offset[2]);
	my @pos2 = ($$matrix[1][0]+$offset[0] , $$matrix[1][1]+$offset[1] , $$matrix[1][2]+$offset[2]);
	my @pos3 = ($$matrix[2][0]+$offset[0] , $$matrix[2][1]+$offset[1] , $$matrix[2][2]+$offset[2]);

	lx("select.drop vertex");
	lx("!!vert.new $offset[0] $offset[1] $offset[2]");
	lx("!!vert.new $pos1[0] $pos1[1] $pos1[2]");
	lx("!!vert.new $pos2[0] $pos2[1] $pos2[2]");
	lx("!!vert.new $pos3[0] $pos3[1] $pos3[2]");

	my $vertCount = lxq("query layerservice vert.n ? all");
	my $vert1 = $vertCount - 4;
	my $vert2 = $vertCount - 3;
	my $vert3 = $vertCount - 2;
	my $vert4 = $vertCount - 1;

	lx("select.drop vertex");
	lx("select.element $mainlayer vertex set $vert1");
	lx("select.element $mainlayer vertex add $vert2");
	lx("select.element $mainlayer vertex add $vert3");
	lx("poly.makeFace");
	lx("select.element $mainlayer vertex set $vert1");
	lx("select.element $mainlayer vertex add $vert3");
	lx("select.element $mainlayer vertex add $vert4");
	lx("poly.makeFace");
	lx("select.element $mainlayer vertex set $vert1");
	lx("select.element $mainlayer vertex add $vert4");
	lx("select.element $mainlayer vertex add $vert2");
	lx("poly.makeFace");
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#PRINT MATRIX (4x4)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#usage : printMatrix(\@matrix);
sub printMatrix{
	lxout("==========");
	for (my $i=0; $i<4; $i++){
		for (my $u=0; $u<4; $u++){
			lxout("[$i][$u] = @{$_[0][$i]}[$u]");
		}
		lxout("\n");
	}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#UNIT VECTOR SUBROUTINE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @unitVector = unitVector(@vector);
sub unitVector{
	my $dist1 = sqrt((@_[0]*@_[0])+(@_[1]*@_[1])+(@_[2]*@_[2]));
	@_ = ((@_[0]/$dist1),(@_[1]/$dist1),(@_[2]/$dist1));
	return @_;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#PERFORM MATH FROM ONE ARRAY TO ANOTHER subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @disp = arrMath(@pos2,@pos1,subt);
sub arrMath{
	my @array1 = (@_[0],@_[1],@_[2]);
	my @array2 = (@_[3],@_[4],@_[5]);
	my $math = @_[6];

	my @newArray;
	if		($math eq "add")	{	@newArray = (@array1[0]+@array2[0],@array1[1]+@array2[1],@array1[2]+@array2[2]);	}
	elsif	($math eq "subt")	{	@newArray = (@array1[0]-@array2[0],@array1[1]-@array2[1],@array1[2]-@array2[2]);	}
	elsif	($math eq "mult")	{	@newArray = (@array1[0]*@array2[0],@array1[1]*@array2[1],@array1[2]*@array2[2]);	}
	elsif	($math eq "div")	{	@newArray = (@array1[0]/@array2[0],@array1[1]/@array2[1],@array1[2]/@array2[2]);	}
	return @newArray;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#4 X 4 MATRIX INVERSION sub
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : @inverseMatrix = inverseMatrix(\@matrix);
sub inverseMatrix{
	my ($m) = $_[0];
	my @matrix = (
		[$$m[0][0],$$m[0][1],$$m[0][2],$$m[0][3]],
		[$$m[1][0],$$m[1][1],$$m[1][2],$$m[1][3]],
		[$$m[2][0],$$m[2][1],$$m[2][2],$$m[2][3]],
		[$$m[3][0],$$m[3][1],$$m[3][2],$$m[3][3]]
	);

	$matrix[0][0] =  $$m[1][1]*$$m[2][2]*$$m[3][3] - $$m[1][1]*$$m[2][3]*$$m[3][2] - $$m[2][1]*$$m[1][2]*$$m[3][3] + $$m[2][1]*$$m[1][3]*$$m[3][2] + $$m[3][1]*$$m[1][2]*$$m[2][3] - $$m[3][1]*$$m[1][3]*$$m[2][2];
	$matrix[1][0] = -$$m[1][0]*$$m[2][2]*$$m[3][3] + $$m[1][0]*$$m[2][3]*$$m[3][2] + $$m[2][0]*$$m[1][2]*$$m[3][3] - $$m[2][0]*$$m[1][3]*$$m[3][2] - $$m[3][0]*$$m[1][2]*$$m[2][3] + $$m[3][0]*$$m[1][3]*$$m[2][2];
	$matrix[2][0] =  $$m[1][0]*$$m[2][1]*$$m[3][3] - $$m[1][0]*$$m[2][3]*$$m[3][1] - $$m[2][0]*$$m[1][1]*$$m[3][3] + $$m[2][0]*$$m[1][3]*$$m[3][1] + $$m[3][0]*$$m[1][1]*$$m[2][3] - $$m[3][0]*$$m[1][3]*$$m[2][1];
	$matrix[3][0] = -$$m[1][0]*$$m[2][1]*$$m[3][2] + $$m[1][0]*$$m[2][2]*$$m[3][1] + $$m[2][0]*$$m[1][1]*$$m[3][2] - $$m[2][0]*$$m[1][2]*$$m[3][1] - $$m[3][0]*$$m[1][1]*$$m[2][2] + $$m[3][0]*$$m[1][2]*$$m[2][1];
	$matrix[0][1] = -$$m[0][1]*$$m[2][2]*$$m[3][3] + $$m[0][1]*$$m[2][3]*$$m[3][2] + $$m[2][1]*$$m[0][2]*$$m[3][3] - $$m[2][1]*$$m[0][3]*$$m[3][2] - $$m[3][1]*$$m[0][2]*$$m[2][3] + $$m[3][1]*$$m[0][3]*$$m[2][2];
	$matrix[1][1] =  $$m[0][0]*$$m[2][2]*$$m[3][3] - $$m[0][0]*$$m[2][3]*$$m[3][2] - $$m[2][0]*$$m[0][2]*$$m[3][3] + $$m[2][0]*$$m[0][3]*$$m[3][2] + $$m[3][0]*$$m[0][2]*$$m[2][3] - $$m[3][0]*$$m[0][3]*$$m[2][2];
	$matrix[2][1] = -$$m[0][0]*$$m[2][1]*$$m[3][3] + $$m[0][0]*$$m[2][3]*$$m[3][1] + $$m[2][0]*$$m[0][1]*$$m[3][3] - $$m[2][0]*$$m[0][3]*$$m[3][1] - $$m[3][0]*$$m[0][1]*$$m[2][3] + $$m[3][0]*$$m[0][3]*$$m[2][1];
	$matrix[3][1] =  $$m[0][0]*$$m[2][1]*$$m[3][2] - $$m[0][0]*$$m[2][2]*$$m[3][1] - $$m[2][0]*$$m[0][1]*$$m[3][2] + $$m[2][0]*$$m[0][2]*$$m[3][1] + $$m[3][0]*$$m[0][1]*$$m[2][2] - $$m[3][0]*$$m[0][2]*$$m[2][1];
	$matrix[0][2] =  $$m[0][1]*$$m[1][2]*$$m[3][3] - $$m[0][1]*$$m[1][3]*$$m[3][2] - $$m[1][1]*$$m[0][2]*$$m[3][3] + $$m[1][1]*$$m[0][3]*$$m[3][2] + $$m[3][1]*$$m[0][2]*$$m[1][3] - $$m[3][1]*$$m[0][3]*$$m[1][2];
	$matrix[1][2] = -$$m[0][0]*$$m[1][2]*$$m[3][3] + $$m[0][0]*$$m[1][3]*$$m[3][2] + $$m[1][0]*$$m[0][2]*$$m[3][3] - $$m[1][0]*$$m[0][3]*$$m[3][2] - $$m[3][0]*$$m[0][2]*$$m[1][3] + $$m[3][0]*$$m[0][3]*$$m[1][2];
	$matrix[2][2] =  $$m[0][0]*$$m[1][1]*$$m[3][3] - $$m[0][0]*$$m[1][3]*$$m[3][1] - $$m[1][0]*$$m[0][1]*$$m[3][3] + $$m[1][0]*$$m[0][3]*$$m[3][1] + $$m[3][0]*$$m[0][1]*$$m[1][3] - $$m[3][0]*$$m[0][3]*$$m[1][1];
	$matrix[3][2] = -$$m[0][0]*$$m[1][1]*$$m[3][2] + $$m[0][0]*$$m[1][2]*$$m[3][1] + $$m[1][0]*$$m[0][1]*$$m[3][2] - $$m[1][0]*$$m[0][2]*$$m[3][1] - $$m[3][0]*$$m[0][1]*$$m[1][2] + $$m[3][0]*$$m[0][2]*$$m[1][1];
	$matrix[0][3] = -$$m[0][1]*$$m[1][2]*$$m[2][3] + $$m[0][1]*$$m[1][3]*$$m[2][2] + $$m[1][1]*$$m[0][2]*$$m[2][3] - $$m[1][1]*$$m[0][3]*$$m[2][2] - $$m[2][1]*$$m[0][2]*$$m[1][3] + $$m[2][1]*$$m[0][3]*$$m[1][2];
	$matrix[1][3] =  $$m[0][0]*$$m[1][2]*$$m[2][3] - $$m[0][0]*$$m[1][3]*$$m[2][2] - $$m[1][0]*$$m[0][2]*$$m[2][3] + $$m[1][0]*$$m[0][3]*$$m[2][2] + $$m[2][0]*$$m[0][2]*$$m[1][3] - $$m[2][0]*$$m[0][3]*$$m[1][2];
	$matrix[2][3] = -$$m[0][0]*$$m[1][1]*$$m[2][3] + $$m[0][0]*$$m[1][3]*$$m[2][1] + $$m[1][0]*$$m[0][1]*$$m[2][3] - $$m[1][0]*$$m[0][3]*$$m[2][1] - $$m[2][0]*$$m[0][1]*$$m[1][3] + $$m[2][0]*$$m[0][3]*$$m[1][1];
	$matrix[3][3] =  $$m[0][0]*$$m[1][1]*$$m[2][2] - $$m[0][0]*$$m[1][2]*$$m[2][1] - $$m[1][0]*$$m[0][1]*$$m[2][2] + $$m[1][0]*$$m[0][2]*$$m[2][1] + $$m[2][0]*$$m[0][1]*$$m[1][2] - $$m[2][0]*$$m[0][2]*$$m[1][1];

	return @matrix;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#4X4 x 4X4 MATRIX MULTIPLY
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : @matrix = mtxMult(\@matrixMult,\@matrix);
#arg0 = transform matrix.  arg1 = matrix to multiply to that then sends the results to the cvar.
sub mtxMult{
	my @matrix = (
		[ @{$_[0][0]}[0]*@{$_[1][0]}[0] + @{$_[0][0]}[1]*@{$_[1][1]}[0] + @{$_[0][0]}[2]*@{$_[1][2]}[0] + @{$_[0][0]}[3]*@{$_[1][3]}[0] , @{$_[0][0]}[0]*@{$_[1][0]}[1] + @{$_[0][0]}[1]*@{$_[1][1]}[1] + @{$_[0][0]}[2]*@{$_[1][2]}[1] + @{$_[0][0]}[3]*@{$_[1][3]}[1] , @{$_[0][0]}[0]*@{$_[1][0]}[2] + @{$_[0][0]}[1]*@{$_[1][1]}[2] + @{$_[0][0]}[2]*@{$_[1][2]}[2] + @{$_[0][0]}[3]*@{$_[1][3]}[2] , @{$_[0][0]}[0]*@{$_[1][0]}[3] + @{$_[0][0]}[1]*@{$_[1][1]}[3] + @{$_[0][0]}[2]*@{$_[1][2]}[3] + @{$_[0][0]}[3]*@{$_[1][3]}[3] ],	#a11b11+a12b21+a13b31+a14b41,a11b12+a12b22+a13b32+a14b42,a11b13+a12b23+a13b33+a14b43,a11b14+a12b24+a13b34+a14b44
		[ @{$_[0][1]}[0]*@{$_[1][0]}[0] + @{$_[0][1]}[1]*@{$_[1][1]}[0] + @{$_[0][1]}[2]*@{$_[1][2]}[0] + @{$_[0][1]}[3]*@{$_[1][3]}[0] , @{$_[0][1]}[0]*@{$_[1][0]}[1] + @{$_[0][1]}[1]*@{$_[1][1]}[1] + @{$_[0][1]}[2]*@{$_[1][2]}[1] + @{$_[0][1]}[3]*@{$_[1][3]}[1] , @{$_[0][1]}[0]*@{$_[1][0]}[2] + @{$_[0][1]}[1]*@{$_[1][1]}[2] + @{$_[0][1]}[2]*@{$_[1][2]}[2] + @{$_[0][1]}[3]*@{$_[1][3]}[2] , @{$_[0][1]}[0]*@{$_[1][0]}[3] + @{$_[0][1]}[1]*@{$_[1][1]}[3] + @{$_[0][1]}[2]*@{$_[1][2]}[3] + @{$_[0][1]}[3]*@{$_[1][3]}[3] ],	#a21b11+a22b21+a23b31+a24b41,a21b12+a22b22+a23b32+a24b42,a21b13+a22b23+a23b33+a24b43,a21b14+a22b24+a23b34+a24b44
		[ @{$_[0][2]}[0]*@{$_[1][0]}[0] + @{$_[0][2]}[1]*@{$_[1][1]}[0] + @{$_[0][2]}[2]*@{$_[1][2]}[0] + @{$_[0][2]}[3]*@{$_[1][3]}[0] , @{$_[0][2]}[0]*@{$_[1][0]}[1] + @{$_[0][2]}[1]*@{$_[1][1]}[1] + @{$_[0][2]}[2]*@{$_[1][2]}[1] + @{$_[0][2]}[3]*@{$_[1][3]}[1] , @{$_[0][2]}[0]*@{$_[1][0]}[2] + @{$_[0][2]}[1]*@{$_[1][1]}[2] + @{$_[0][2]}[2]*@{$_[1][2]}[2] + @{$_[0][2]}[3]*@{$_[1][3]}[2] , @{$_[0][2]}[0]*@{$_[1][0]}[3] + @{$_[0][2]}[1]*@{$_[1][1]}[3] + @{$_[0][2]}[2]*@{$_[1][2]}[3] + @{$_[0][2]}[3]*@{$_[1][3]}[3] ],	#a31b11+a32b21+a33b31+a34b41,a31b12+a32b22+a33b32+a34b42,a31b13+a32b23+a33b33+a34b43,a31b14+a32b24+a33b34+a34b44
		[ @{$_[0][3]}[0]*@{$_[1][0]}[0] + @{$_[0][3]}[1]*@{$_[1][1]}[0] + @{$_[0][3]}[2]*@{$_[1][2]}[0] + @{$_[0][3]}[3]*@{$_[1][3]}[0] , @{$_[0][3]}[0]*@{$_[1][0]}[1] + @{$_[0][3]}[1]*@{$_[1][1]}[1] + @{$_[0][3]}[2]*@{$_[1][2]}[1] + @{$_[0][3]}[3]*@{$_[1][3]}[1] , @{$_[0][3]}[0]*@{$_[1][0]}[2] + @{$_[0][3]}[1]*@{$_[1][1]}[2] + @{$_[0][3]}[2]*@{$_[1][2]}[2] + @{$_[0][3]}[3]*@{$_[1][3]}[2] , @{$_[0][3]}[0]*@{$_[1][0]}[3] + @{$_[0][3]}[1]*@{$_[1][1]}[3] + @{$_[0][3]}[2]*@{$_[1][2]}[3] + @{$_[0][3]}[3]*@{$_[1][3]}[3] ]	#a41b11+a42b21+a43b31+a44b41,a41b12+a42b22+a43b32+a44b42,a41b13+a42b23+a43b33+a44b43,a41b14+a42b24+a43b34+a44b44
	);

	return @matrix;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#4X4 x 1x3 MATRIX MULTIPLY (move vert by 4x4 matrix)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : @vertPos = vec_mtxMult(\@matrix,\@vertPos);
#arg0 = transform matrix.  arg1 = vertPos to multiply to that then sends the results to the cvar.
sub vec_mtxMult{
	my @pos = (
		@{$_[0][0]}[0]*@{$_[1]}[0] + @{$_[0][0]}[1]*@{$_[1]}[1] + @{$_[0][0]}[2]*@{$_[1]}[2] + @{$_[0][0]}[3],	#a1*x_old + a2*y_old + a3*z_old + a4
		@{$_[0][1]}[0]*@{$_[1]}[0] + @{$_[0][1]}[1]*@{$_[1]}[1] + @{$_[0][1]}[2]*@{$_[1]}[2] + @{$_[0][1]}[3],	#b1*x_old + b2*y_old + b3*z_old + b4
		@{$_[0][2]}[0]*@{$_[1]}[0] + @{$_[0][2]}[1]*@{$_[1]}[1] + @{$_[0][2]}[2]*@{$_[1]}[2] + @{$_[0][2]}[3]	#c1*x_old + c2*y_old + c3*z_old + c4
	);

	#dividing @pos by (matrix's 4,4) to correct "projective space"
	$pos[0] = $pos[0] / @{$_[0][3]}[3];
	$pos[1] = $pos[1] / @{$_[0][3]}[3];
	$pos[2] = $pos[2] / @{$_[0][3]}[3];

	return @pos;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CROSSPRODUCT SUBROUTINE (ver 1.1)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @crossProduct = crossProduct(\@vector1,\@vector2);
sub crossProduct{
	return ( (${$_[0]}[1]*${$_[1]}[2])-(${$_[1]}[1]*${$_[0]}[2]) , (${$_[0]}[2]*${$_[1]}[0])-(${$_[1]}[2]*${$_[0]}[0]) , (${$_[0]}[0]*${$_[1]}[1])-(${$_[1]}[0]*${$_[0]}[1]) );
}


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#SORT ROWS SETUP subroutine  (0 and -1 are dupes if it's a loop)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE :
#requires SORTROW sub
#sortRowStartup(dontFormat,@edges);			#NO FORMAT
#sortRowStartup(edgesSelected,@edges);		#EDGES SELECTED
#sortRowStartup(@edges);					#SELECTION ? EDGE
sub sortRowStartup{

	#------------------------------------------------------------
	#Import the edge list and format it.
	#------------------------------------------------------------
	my @origEdgeList = @_;
	my $edgeQueryMode = shift(@origEdgeList);
	#------------------------------------------------------------
	#(NO) formatting
	#------------------------------------------------------------
	if ($edgeQueryMode eq "dontFormat"){
		#don't format!
	}
	#------------------------------------------------------------
	#(edges ? selected) formatting
	#------------------------------------------------------------
	elsif ($edgeQueryMode eq "edgesSelected"){
		tr/()//d for @origEdgeList;
	}
	#------------------------------------------------------------
	#(selection ? edge) formatting
	#------------------------------------------------------------
	else{
		my @tempEdgeList;
		foreach my $edge (@origEdgeList){	if ($edge =~ /\($mainlayer/){	push(@tempEdgeList,$edge);		}	}
		#[remove layer info] [remove ( ) ]
		@origEdgeList = @tempEdgeList;
		s/\(\d{0,},/\(/  for @origEdgeList;
		tr/()//d for @origEdgeList;
	}


	#------------------------------------------------------------
	#array creation (after the formatting)
	#------------------------------------------------------------
	our @origEdgeList_edit = @origEdgeList;
	our @vertRow=();
	our @vertRowList=();

	our @vertList=();
	our %vertPosTable=();
	our %endPointVectors=();

	our @vertMergeOrder=();
	our @edgesToRemove=();
	our $removeEdges = 0;


	#------------------------------------------------------------
	#Begin sorting the [edge list] into different [vert rows].
	#------------------------------------------------------------
	while (($#origEdgeList_edit + 1) != 0)
	{
		#this is a loop to go thru and sort the edge loops
		@vertRow = split(/,/, @origEdgeList_edit[0]);
		shift(@origEdgeList_edit);
		&sortRow;

		#take the new edgesort array and add it to the big list of edges.
		push(@vertRowList, "@vertRow");
	}


	#Print out the DONE list   [this should normally go in the sorting sub]
	#lxout("- - -DONE: There are ($#vertRowList+1) edge rows total");
	#for ($i = 0; $i < @vertRowList; $i++) {	lxout("- - -vertRow # ($i) = @vertRowList[$i]"); }
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#SORT ROWS subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE :
#requires sortRowStartup sub.
sub sortRow
{
	#this first part is stupid.  I need it to loop thru one more time than it will:
	my @loopCount = @origEdgeList_edit;
	unshift (@loopCount,1);

	foreach(@loopCount)
	{
		#lxout("[->] USING sortRow subroutine----------------------------------------------");
		#lxout("original edge list = @origEdgeList");
		#lxout("edited edge list =  @origEdgeList_edit");
		#lxout("vertRow = @vertRow");
		my $i=0;
		foreach my $thisEdge(@origEdgeList_edit)
		{
			#break edge into an array  and remove () chars from array
			@thisEdgeVerts = split(/,/, $thisEdge);
			#lxout("-        origEdgeList_edit[$i] Verts: @thisEdgeVerts");

			if (@vertRow[0] == @thisEdgeVerts[0])
			{
				#lxout("edge $i is touching the vertRow");
				unshift(@vertRow,@thisEdgeVerts[1]);
				splice(@origEdgeList_edit, $i,1);
				last;
			}
			elsif (@vertRow[0] == @thisEdgeVerts[1])
			{
				#lxout("edge $i is touching the vertRow");
				unshift(@vertRow,@thisEdgeVerts[0]);
				splice(@origEdgeList_edit, $i,1);
				last;
			}
			elsif (@vertRow[-1] == @thisEdgeVerts[0])
			{
				#lxout("edge $i is touching the vertRow");
				push(@vertRow,@thisEdgeVerts[1]);
				splice(@origEdgeList_edit, $i,1);
				last;
			}
			elsif (@vertRow[-1] == @thisEdgeVerts[1])
			{
				#lxout("edge $i is touching the vertRow");
				push(@vertRow,@thisEdgeVerts[0]);
				splice(@origEdgeList_edit, $i,1);
				last;
			}
			else
			{
				$i++;
			}
		}
	}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#RETURN BORDER EDGES FROM POLY LIST
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : my @borderEdges = returnBorderEdges(\@polys);
sub returnBorderEdges{
	my %edgeList;
	foreach my $poly (@{$_[0]}){
		my @verts = lxq("query layerservice poly.vertList ? $poly");
		for (my $i=-1; $i<$#verts; $i++){
			my $edge;
			if (@verts[$i]<@verts[$i+1])	{	$edge = @verts[$i].",".@verts[$i+1];	}
			else							{	$edge = @verts[$i+1].",".@verts[$i];	}
			$edgeList{$edge} += 1;
		}
	}

	foreach my $key (keys %edgeList)	{	if ($edgeList{$key} != 1)	{	delete $edgeList{$key};	}	}
	return (keys %edgeList);
}
