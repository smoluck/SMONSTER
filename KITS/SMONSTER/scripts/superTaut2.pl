#perl
#SUPER TAUT PART TWO!
#AUTHOR: Seneca Menard
#version 3.2

#This script is an addition to the superTaut script.  What it's for is planar tauts, and that means aligning your selection to the last selected poly's plane.
#VERT MODE :
#1) : vert + planar taut = it snaps the verts to the last poly's plane, using the angle that the poly normal defines.
#2) : vert + axis taut = it snaps the verts to the last poly's plane, using the chosen axis (X,Y,Z) as the angle.
#3) : vert + planart taut (top or bottom) = top or bottom is only for edges, so it just runs a normal planar taut.
#4) : vert + single angle taut = it snaps all the verts to last poly's plane, using the angle defined by the first two selected verts.
#EDGE MODE :
#1) : edge + planar taut = it snaps the closest vert on each edge to the last poly's plane, using each edge to define each angle.
#2) : edge + axis taut = it snaps all the edges' verts to the last poly's plane, using the chosen axis (X,Y,Z) as the angle.
#3) : edge + planar taut (top or bottom) what this does is similar to 1), only instead of moving the closest edgeverts to the plane, it moves only the top or bottom edge verts.
#4) : edge + single angle taut = does nothing.  this is only for vert mode.
#POLY MODE :
#1) : poly + planar taut = it snaps all the polys' verts to the last poly's plane, using the last poly's normal as the angle.
#2) : poly + axis taut = it snaps all the polys' vers tot he last poly's plane, using the chosen axis (X,Y,Z) as the angle.
#3) : poly + planar taut (top or bottom) = top or bottom is only for edges, so it's just like running a normal planar taut.
#4) : poly + single angle taut  = does nothing.  this is only for vert mode.

#(3-22-07 feature+fix) : If you only have one poly selected and are in polygon mode, it will now guess that you didn't want to perform a polygonal planar taut and will try to perform an edge or vert planar taut instead.  I also removed a small bug with polygonal planar taut not using the correct poly list.
#(8-20-08 fix) : removed my prior fix for the measurement unit system and put in the correct one.

#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																	SAFETY CHECKS																====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
my $mainlayer = lxq("query layerservice layers ? main");
my $mainlayerID = lxq("query layerservice layer.id ? $mainlayer");
my @polys = lxq("query layerservice polys ? selected");
my @normal;
my @polyPos;
my $flipPoly;
#symm
our $symmAxis = lxq("select.symmetryState ?");
if 		($symmAxis eq "none")	{	$symmAxis = 3;	}
elsif	($symmAxis eq "x")		{	$symmAxis = 0;	}
elsif	($symmAxis eq "y")		{	$symmAxis = 1;	}
elsif	($symmAxis eq "z")		{	$symmAxis = 2;	}
if ($symmAxis != 3){
	lx("select.symmetryState none");
}

#Remember what the workplane was
@WPmem[0] = lxq ("workPlane.edit cenX:? ");
@WPmem[1] = lxq ("workPlane.edit cenY:? ");
@WPmem[2] = lxq ("workPlane.edit cenZ:? ");
@WPmem[3] = lxq ("workPlane.edit rotX:? ");
@WPmem[4] = lxq ("workPlane.edit rotY:? ");
@WPmem[5] = lxq ("workPlane.edit rotZ:? ");
lx("workPlane.reset ");

#layer reference (modded.  only references if not in item mode)
my $layerReference = lxq("layer.setReference ?");
lx("!!layer.setReference $mainlayerID");


#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																SCRIPT ARGUMENTS																====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
foreach my $arg (@ARGV){
	if		($arg =~ /x/i)			{	our $rayAxis = "x";		}
	elsif	($arg =~ /y/i)			{	our $rayAxis = "y";		}
	elsif	($arg =~ /z/i)			{	our $rayAxis = "z";		}
	elsif	($arg =~ /over/i)		{	our $forcePos = 1;		}
	elsif	($arg =~ /under/i)		{	our $forcePos = -1;		}
	elsif	($arg =~ /vector/i)		{	our $forceVector = 1;	}
}




#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																	SELECTION SETUP																====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
if (@polys == 0){die("\n.\n[------------------------------------You don't have any POLYS selected so I'm killing the script-----------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");}

if ( lxq( "select.typeFrom {vertex;edge;polygon;item} ?" ) ){
	&vertMode;
}
elsif( lxq( "select.typeFrom {edge;polygon;item;vertex} ?" ) ){
	&edgeMode;
}
elsif( lxq( "select.typeFrom {polygon;item;vertex;edge} ?" ) ){
	if ((($symmAxis != 3) && (@polys > 2)) || (($symmAxis == 3) && (@polys > 1))){
		&polyMode;
	}else{
		if (lxq("query layerservice edge.n ? selected") > 1){
			if ($forceVector == 1){
				lx("select.type vertex");
				&vertMode;
			}else{
				lx("select.type edge");
				&edgeMode;
			}
		}elsif (lxq("query layerservice vert.n ? selected") > 1){
			lx("select.type vertex");
			&vertMode;
		}elsif (@polys == 2){
			&polyMode;
		}else{
			die("\n.\n[-------You only have 1 poly selected and don't have any verts or edges selected, so I can't do ANY planar tauts-------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}
	}
}
else{
	die("\n.\n[---------------------------------------------You're not in vert, edge, or polygon mode.--------------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
}


#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																	SELECTION MODES																====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================



#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#VERT MODE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub vertMode{
	my @verts = lxq("query layerservice verts ? selected");
	#SYMMETRY OFF
	if ($symmAxis == 3){
		#VECTOR ALIGN
		if ($forceVector == 1){
			lxout("[->] Align verts using the single vector defined by the first two verts");
			&intersectRayPlane(symmOff,force,@polys[-1],@verts);
		}

		#AXIS ALIGN
		elsif ($rayAxis =~ /[x-z]/i){
			lxout("[->] Align verts to plane in single axis ($rayAxis)");
			&intersectRayPlane(symmOff,axis,@polys[-1],@verts);
		}

		#N ALIGN
		else{
			lxout("[->] Align verts to plane in plane normal space");
			&intersectVertPlane(symmOff,@polys[-1],@verts);
		}
	}

	#SYMMETRY ON
	else{
		my ($vertsPos,$vertsNeg) = sortSymm(vert,@verts);
		my @polyPos = lxq("query layerservice poly.pos ? @polys[-1]");
		if	((@$vertsPos == 0) && (@$vertsNeg > 0) && (@polyPos[$symmAxis] > 0)){$flipPoly = 1;}
		elsif ((@$vertsPos > 0) && (@polyPos[$symmAxis] < 0)){$flipPoly = 1;}

		#POSITIVE HALF
		if (@$vertsPos > 0){
			#VECTOR ALIGN
			if ($forceVector == 1){
				lxout("[->] (symm pos) Align verts using the single vector defined by the first two verts");
				&intersectRayPlane(symmOff,force,@polys[-1],@$vertsPos);
			}

			#AXIS ALIGN
			elsif ($rayAxis =~ /[x-z]/i){
				lxout("[->] (symm pos) Align verts to plane in single axis ($rayAxis)");
				&intersectRayPlane(symmOff,axis,@polys[-1],@$vertsPos);
			}

			#N ALIGN
			else{
				lxout("[->] (symm pos) Align verts to plane in plane normal space");
				&intersectVertPlane(symmOff,@polys[-1],@$vertsPos);
			}
		}

		#NEGATIVE HALF
		if (@$vertsNeg > 0){
			#VECTOR ALIGN
			if ($forceVector == 1){
				lxout("[->] (symm neg) Align verts using the single vector defined by the first two verts");
				&intersectRayPlane(symmOn,force,@polys[-1],@$vertsNeg);
			}

			#AXIS ALIGN
			elsif ($rayAxis =~ /[x-z]/i){
				lxout("[->] (symm neg) Align verts to plane in single axis ($rayAxis)");
				&intersectRayPlane(symmOn,axis,@polys[-1],@$vertsNeg);
			}

			#N ALIGN
			else{
				lxout("[->] (symm neg) Align verts to plane in plane normal space");
				&intersectVertPlane(symmOn,@polys[-1],@$vertsNeg);
			}
		}
	}

	#RESTORE SELECTION AND CLEANUP
	lx("select.drop vertex");
	foreach my $vert (@verts){lx("select.element $mainlayer vertex add $vert");}
	&cleanup;
}



#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#EDGE MODE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub edgeMode{
	if ($forceVector == 1){die("\n.\n[----------------(single angle) planar taut's only for verts.  You're not in vert mode so I'm killing the script------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");}
	our @edges = lxq("query layerservice edges ? selected");

	#SYMMETRY OFF
	if ($symmAxis == 3){
		#AXIS ALIGN
		if ($rayAxis =~ /[x-z]/i){
			lxout("[->] Align edges (verts) to plane in single axis ($rayAxis)");
			my @verts = getVertList(edge,\@edges);
			&intersectRayPlane(symmOff,axis,@polys[-1],@verts);
		}

		#RAY ALIGN
		else{
			lxout("[->] Align edges to plane");
			&intersectRayPlane(symmOff,ray,@polys[-1],@edges);
		}
	}

	#SYMMETRY ON
	else{
		my ($edgesPos,$edgesNeg) = sortSymm(edge,@edges);
		my @polyPos = lxq("query layerservice poly.pos ? @polys[-1]");
		if	((@$edgesPos == 0) && (@$edgesNeg > 0) && (@polyPos[$symmAxis] > 0)){$flipPoly = 1;}
		elsif ((@$edgesPos > 0) && (@polyPos[$symmAxis] < 0)){$flipPoly = 1;}

		#POSITIVE HALF
		if (@$edgesPos > 0){
			#AXIS ALIGN
			if ($rayAxis =~ /[x-z]/i){
				lxout("[->] Align edges (verts) to plane in single axis ($rayAxis)");
				my @verts = getVertList(edge,\@$edgesPos);
				&intersectRayPlane(symmOff,axis,@polys[-1],@verts);
			}

			#RAY ALIGN
			else{
				lxout("[->] Align edges to plane");
				&intersectRayPlane(symmOff,ray,@polys[-1],@$edgesPos);
			}
		}

		#NEGATIVE HALF
		if (@$edgesNeg > 0){
			#AXIS ALIGN
			if ($rayAxis =~ /[x-z]/i){
				lxout("[->] Align edges (verts) to plane in single axis ($rayAxis)");
				my @verts = getVertList(edge,\@$edgesNeg);
				&intersectRayPlane(symmOn,axis,@polys[-1],@verts);
			}

			#RAY ALIGN
			else{
				lxout("[->] Align edges to plane");
				&intersectRayPlane(symmOn,ray,@polys[-1],@$edgesNeg);
			}
		}
	}

	#RESTORE SELECTION AND CLEANUP;
	lx("select.type edge");
	&cleanup;
}



#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#POLY MODE
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub polyMode{
	if ($forceVector == 1){die("\n.\n[----------------(single angle) planar taut's only for verts.  You're not in vert mode so I'm killing the script------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");}

	#SYMMETRY OFF
	if ($symmAxis == 3){

		#AXIS ALIGN
		if ($rayAxis =~ /[x-z]/i){
			my @newPolyList = @polys;
			pop(@newPolyList);
			my @verts = getVertList(poly,\@newPolyList);
			&intersectRayPlane(symmOff,axis,@polys[-1],@verts);
		}

		#RAY ALIGN
		else{
			my @newPolyList = @polys;
			pop(@newPolyList);
			my @verts = getVertList(poly,\@newPolyList);
			&intersectVertPlane(symmOff,@polys[-1],@verts);
		}
	}

	#SYMMETRY ON
	else{

		#SETUP : find key poly
		my ($polysPos,$polysNeg) = sortSymm(poly,@polys);
		if (@$polysPos == @$polysNeg){
			$keyPoly = pop(@$polysPos);							#if A=B or B=A
			pop(@$polysNeg);
		}elsif((@$polysPos ==1) && (@$polysNeg > @$polysPos)){	#if A=1 and B>A
			$keyPoly = pop(@$polysPos);
		}elsif((@$polysNeg ==1) && (@$polysPos > @$polysNeg)){	#if B=1 and A>B
			$keyPoly = pop(@$polysNeg);
		}elsif(@$polysPos == @$polysNeg+1){						#if A=B+1
			$keyPoly = pop(@$polysPos);
		}elsif(@$polysNeg == @$polysPos+1){						#if B=A+1
			$keyPoly = pop(@$polysNeg);
		}
		#SETUP : flip poly if needed.
		my @polyPos = lxq("query layerservice poly.pos ? $keyPoly");
		if ((@$polysPos > 0) && (@polyPos[$symmAxis] < 1)){$flipPoly = 1;}
		elsif ((@$polysPos == 0) && (@$polysNeg > 0) && (@polyPos[$symmAxis] > 0)){$flipPoly = 1;}


		#POSITIVE HALF
		if (@$polysPos > 0){
			#AXIS ALIGN
			if ($rayAxis =~ /[x-z]/i){
				my @verts = getVertList(poly,\@$polysPos);
				&intersectRayPlane(symmOff,axis,$keyPoly,@verts);
			}

			#RAY ALIGN
			else{
				my @verts = getVertList(poly,\@$polysPos);
				&intersectVertPlane(symmOff,$keyPoly,@verts);
			}
		}

		#POSITIVE HALF
		if (@$polysNeg > 0){
			#AXIS ALIGN
			if ($rayAxis =~ /[x-z]/i){
				my @verts = getVertList(poly,\@$polysNeg);
				&intersectRayPlane(symmOn,axis,$keyPoly,@verts);
			}

			#RAY ALIGN
			else{
				my @verts = getVertList(poly,\@$polysNeg);
				&intersectVertPlane(symmOn,$keyPoly,@verts);
			}
		}
	}

	#RESTORE SELECTION AND CLEANUP;
	lx("select.type polygon");
	&cleanup;
}



#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																	MAIN ROUTINES																	====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#INTERSECT VERT AND PLANE subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub intersectVertPlane{  #TEMP : can be sped up by just using stretch...
	lx("select.type vertex");
	my $symmState = shift(@_);
	if (($symmState eq "symmOff") || (@normal == 0)){
		lxout("[->] intersect vert plane (says symmetry is off)");
		my $poly = shift(@_);
		@normal = lxq("query layerservice poly.normal ? $poly");
		@polyPos = lxq("query layerservice poly.pos ? $poly");
		if ($flipPoly == 1){&flipPoly;}
	}else{
		lxout("[->] intersect vert plane (says symmetry is on and this is round 2)");
		shift(@_);
		&flipPoly;
	}
	my $planeDist = dotProduct(\@normal,\@polyPos);

	foreach my $vert (@_){
		my @pos = lxq("query layerservice vert.pos ? $vert");
		my $dp =  -1 * (dotProduct(\@pos,\@normal)-$planeDist);
		lx("select.element $mainlayer vertex set $vert");
		my @moveToPos = arrMath(@pos,arrMath(@normal,$dp,$dp,$dp,mult),add);
		lx("vert.set x {@moveToPos[0]}");
		lx("vert.set y {@moveToPos[1]}");
		lx("vert.set z {@moveToPos[2]}");
	}
}


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#INTERSECT RAY AND PLANE subroutine (brand new)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub intersectRayPlane{

	#SETUP
	lx("select.type vertex");
	my $symmState = shift(@_);
	my $mode = shift(@_);
	if (($symmState eq "symmOff") || (@normal == 0)){
		lxout("[->] intersect ray plane (says symmetry is off)");
		my $poly = shift(@_);
		@normal = lxq("query layerservice poly.normal ? $poly");
		@polyPos = lxq("query layerservice poly.pos ? $poly");
		if ($flipPoly == 1){&flipPoly;}
	}else{
		lxout("[->] intersect ray plane (says symmetry is on and this is round 2)");
		shift(@_);
		&flipPoly;
	}
	my $planeDist = -1 * dotProduct(\@normal,\@polyPos);

	#AXIS DEPENDENT RAY TO PLANE
	if ($mode eq "axis"){
		foreach my $vert (@_){
			my @pos1 = lxq("query layerservice vert.pos ? $vert");
			my @pos2;
			if		($rayAxis =~ /x/i)	{ @pos2 = (@pos1[0]-1,@pos1[1],@pos1[2]); }
			elsif	($rayAxis =~ /y/i)	{ @pos2 = (@pos1[0],@pos1[1]-1,@pos1[2]); }
			else					{ @pos2 = (@pos1[0],@pos1[1],@pos1[2]-1); }

			my @disp = arrMath(@pos2,@pos1,subt);
			my $test1 = -1 * (dotProduct(\@pos1,\@normal)+$planeDist);
			my $test2 = dotProduct(\@disp,\@normal);
			my $time;
			if ( ($test1 != 0) && ($test2 != 0) ){
				$time = $test1/$test2;
			}else{
				lx("skipping this vert ($vert) because it's coplanar with the poly");
				next;
			}
			my @intersectPoint = arrMath(@pos1,arrMath(@disp,$time,$time,$time,mult),add);
			lx("select.element $mainlayer vertex set $vert");
			lx("vert.set x {@intersectPoint[0]}");
			lx("vert.set y {@intersectPoint[1]}");
			lx("vert.set z {@intersectPoint[2]}");
		}
	}

	#FORCED RAY TO PLANE
	elsif ($mode eq "force"){
		my $vert0 = shift(@_);
		my @pos0 = lxq("query layerservice vert.pos ? $vert0");
		my @pos1 = lxq("query layerservice vert.pos ? @_[0]");
		my @forcedVector = arrMath(@pos1,@pos0,subt);

		foreach my $vert (@_){
			my @pos1 = lxq("query layerservice vert.pos ? $vert");
			my @disp = @forcedVector;
			my $test1 = -1 * (dotProduct(\@pos1,\@normal)+$planeDist);
			my $test2 = dotProduct(\@disp,\@normal);
			my $time;
			if ( ($test1 != 0) && ($test2 != 0) ){
				$time = $test1/$test2;
			}else{
				lx("skipping this vert ($vert) because it's coplanar with the poly");
				next;
			}
			my @intersectPoint = arrMath(@pos1,arrMath(@disp,$time,$time,$time,mult),add);
			lx("select.element $mainlayer vertex set $vert");
			lx("vert.set x {@intersectPoint[0]}");
			lx("vert.set y {@intersectPoint[1]}");
			lx("vert.set z {@intersectPoint[2]}");
		}
	}

	#TRUE RAY TO PLANE
	else{
		foreach my $edge (@_){
			my @verts = split(/[^0-9]/,$edge);
			my $keyVert;

			#determine how to set the edges.  (greater?  lessthan?  closest?)
			my @pos1= lxq("query layerservice vert.pos ? @verts[1]");
			my @pos2 = lxq("query layerservice vert.pos ? @verts[2]");
			if ($forcePos != 0){
				my $polyDist1 =  -1 * (dotProduct(\@pos1,\@normal) - $planeDist);
				my $polyDist2 =  -1 * (dotProduct(\@pos2,\@normal) - $planeDist);
				if ($forcePos == 1){
					if (abs($polyDist1) < abs($polyDist2))	{	$keyVert = @verts[1];	}
					else								{	$keyVert = @verts[2];	}
				}else{
					if (abs($polyDist1) > abs($polyDist2))	{	$keyVert = @verts[1];	}
					else								{	$keyVert = @verts[2];	}
				}
			}else{
				my $polyDist1 =  -1 * (dotProduct(\@pos1,\@normal) - (-1*$planeDist));
				my $polyDist2 =  -1 * (dotProduct(\@pos2,\@normal) - (-1*$planeDist));
				if (abs($polyDist1) < abs($polyDist2))	{	$keyVert = @verts[1];	}
				else								{	$keyVert = @verts[2];	}
			}

			my @disp = arrMath(@pos2,@pos1,subt);
			my $test1 = -1 * (dotProduct(\@pos1,\@normal)+$planeDist);
			my $test2 = dotProduct(\@disp,\@normal);
			my $time;
			if ( ($test1 != 0) && ($test2 != 0) ){
				$time = $test1/$test2;
			}else{
				lx("skipping this vert ($vert) because it's coplanar with the poly");
				next;
			}
			my @intersectPoint = arrMath(@pos1,arrMath(@disp,$time,$time,$time,mult),add);
			lx("select.element $mainlayer vertex set $keyVert");
			lx("vert.set x {@intersectPoint[0]}");
			lx("vert.set y {@intersectPoint[1]}");
			lx("vert.set z {@intersectPoint[2]}");
		}
	}
}



#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#===																	SUBROUTINES																	====
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================
#=====================================================================================================================================


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#FLIP THE POLY DATA FOR SYMMETRY OR IF A NEGATIVE POLYS SELECTED
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub flipPoly{
	lxout("[->] Running flip poly subroutine");
	if ($symmAxis == 0){
		@normal = arrMath(@normal,-1,1,1,mult);
		@polyPos = arrMath(@polyPos,-1,1,1,mult);
	}
	elsif ($symmAxis == 1){
		@normal = arrMath(@normal,1,-1,1,mult);
		@polyPos = arrMath(@polyPos,1,-1,1,mult);
	}
	else{
		@normal = arrMath(@normal,1,1,-1,mult);
		@polyPos = arrMath(@polyPos,1,1,-1,mult);
	}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CONVERT POLY OR EDGE LIST INTO VERT LIST.
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub getVertList{
	my $selType = @_[0];
	my %elemList;
	foreach my $elem (@{$_[1]}){
		my @verts = lxq("query layerservice $selType.vertList ? $elem");
		foreach my $vert (@verts){	$elemList{$vert}=1;}
	}
	return(keys %elemList);
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#SORT THE ELEMENTS INTO SYMMETRICAL HALVES (requires $symmAxis)
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub sortSymm{
	my $selType = shift(@_);
	my @positive;
	my @negative;

	foreach my $elem (@_){
		my @pos = lxq("query layerservice $selType.pos ? $elem");
		if (@pos[$symmAxis] > 0 )	{  push(@positive,$elem);		}
		else					{  push(@negative,$elem);	}

	}
	return(\@positive,\@negative);
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
#PERFORM MATH FROM ONE ARRAY TO ANOTHER subroutine
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub arrMath{
	my @array1 = (@_[0],@_[1],@_[2]);
	my @array2 = (@_[3],@_[4],@_[5]);
	my $math = @_[6];
	my @newArray;
	if ($math eq "add")		{	@newArray = (@array1[0]+@array2[0],@array1[1]+@array2[1],@array1[2]+@array2[2]);	}
	elsif ($math eq "subt")	{	@newArray = (@array1[0]-@array2[0],@array1[1]-@array2[1],@array1[2]-@array2[2]);	}
	elsif ($math eq "mult")	{	@newArray = (@array1[0]*@array2[0],@array1[1]*@array2[1],@array1[2]*@array2[2]);	}
	elsif ($math eq "div")		{	@newArray = (@array1[0]/@array2[0],@array1[1]/@array2[1],@array1[2]/@array2[2]);	}
	return @newArray;
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#POPUP SUB
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : popup("What I wanna print");
sub popup #(MODO2 FIX)
{
	lx("dialog.setup yesNo");
	lx("dialog.msg {@_}");
	lx("dialog.open");
	my $confirm = lxq("dialog.result ?");
	if($confirm eq "no"){die;}
}

#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#CLEANUP SUB
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
sub cleanup{
	#Set the layer reference back
	lx("!!layer.setReference [$layerReference]");

	#put the WORKPLANE and UNIT MODE back to what you were in before.
	lx("workPlane.edit {@WPmem[0]} {@WPmem[1]} {@WPmem[2]} {@WPmem[3]} {@WPmem[4]} {@WPmem[5]}");

	#Set Symmetry back
	if ($symmAxis != 3)
	{
		#CONVERT MY OLDSCHOOL SYMM AXIS TO MODO's NEWSCHOOL NAME
		if 		($symmAxis == "3")	{	$symmAxis = "none";	}
		elsif	($symmAxis == "0")	{	$symmAxis = "x";		}
		elsif	($symmAxis == "1")	{	$symmAxis = "y";		}
		elsif	($symmAxis == "2")	{	$symmAxis = "z";		}
		lxout("turning symm back on ($symmAxis)"); lx("!!select.symmetryState $symmAxis");
	}
}