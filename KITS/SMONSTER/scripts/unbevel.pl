#perl
#UNBEVEL
#version 1.31
#AUTHOR: Seneca Menard

#This script is to unbevel edges.  You must have one extra edge selected on each side of the bevel, to tell me what edges are "flat" taht you want to unbevel to.
#You can unbevel more than one edgerow at a time, you just have to make sure that the different edgerows aren't touching.

#(8-8-06) : now works on items that have been translated
#(11-14-06) : I reorder the layer reference command to hide modo's workplane flip bug.
#(9-9-07) : I added a progress bar
#(8-1-08) : I swapped the [] for {} so that the numbers would always be read as meters and then was able to remove my temp preference change that was previously there to fix that.
#(3-25-11 fix) : 501 sp2 had an annoying syntax change.  grrr.
#(6-1-12 feature) : resize : you can now scale the bevels instead of deleting them.
#(1-10-14 fix) : got the actr storage system up to date with 601

#SCRIPT ARGUMENTS :
# "resize" : this is so you can scale your bevels instead of deleting them.  quite handy actually.  too bad it's not interactive.  :P
# "noVertMerge" : turns off vert merging

my $mainlayer = lxq("query layerservice layers ? main");
my $modoBuild = lxq("query platformservice appbuild ?");
if ($modoBuild > 41320){our $selectPolygonArg = "psubdiv";}else{our $selectPolygonArg = "curve";}
our @origEdgeList = lxq("query layerservice edges ? selected");
our @origEdgeList_edit;
our @vertRow;
our @vertRowList;
our $scaleAmount = 0;


#-----------------------------------------------------------------------------------------------------------
#SCRIPT ARGUMENTS
#-----------------------------------------------------------------------------------------------------------
foreach my $arg (@ARGV){
	if ($arg =~ /resize/i)		{	$scaleAmount = quickDialog("scale amount",float,.5,0,1000000);	}
	if ($arg =~ /noVertMerge/i)	{	our $noVertMerge = 1;											}
}


#-----------------------------------------------------------------------------------------------------------
#CREATE AND EDIT the edge list.  [remove ( )] (FIXED FOR M2.  I'm not using the multilayer query anymore)
#-----------------------------------------------------------------------------------------------------------
s/\(// for @origEdgeList;
s/\)// for @origEdgeList;
@origEdgeList_edit = @origEdgeList;


#-----------------------------------------------------------------------------------------------------------
#SAFETY CHECKS
#-----------------------------------------------------------------------------------------------------------
#Turn off and protect Symmetry
my $symmAxis = lxq("select.symmetryState ?");
#CONVERT THE SYMM AXIS TO MY OLDSCHOOL NUMBER
if 		($symmAxis eq "none")	{	$symmAxis = 3;	}
elsif	($symmAxis eq "x")		{	$symmAxis = 0;	}
elsif	($symmAxis eq "y")		{	$symmAxis = 1;	}
elsif	($symmAxis eq "z")		{	$symmAxis = 2;	}
if 		($symmAxis != 3)		{	lx("select.symmetryState none");	}

#Remember what the workplane was and turn it off
my @WPmem;
@WPmem[0] = lxq ("workPlane.edit cenX:? ");
@WPmem[1] = lxq ("workPlane.edit cenY:? ");
@WPmem[2] = lxq ("workPlane.edit cenZ:? ");
@WPmem[3] = lxq ("workPlane.edit rotX:? ");
@WPmem[4] = lxq ("workPlane.edit rotY:? ");
@WPmem[5] = lxq ("workPlane.edit rotZ:? ");
lx("!!workPlane.reset ");


#-----------------------------------------------------------------------------------
#REMEMBER SELECTION SETTINGS and then set it to selectauto  ((MODO6 FIX))
#-----------------------------------------------------------------------------------
#sets the ACTR preset
my $seltype;
my $selAxis;
my $selCenter;
my $actr = 1;

if   ( lxq( "tool.set actr.auto ?") eq "on")			{	$seltype = "actr.auto";			}
elsif( lxq( "tool.set actr.select ?") eq "on")			{	$seltype = "actr.select";		}
elsif( lxq( "tool.set actr.border ?") eq "on")			{	$seltype = "actr.border";		}
elsif( lxq( "tool.set actr.selectauto ?") eq "on")		{	$seltype = "actr.selectauto";	}
elsif( lxq( "tool.set actr.element ?") eq "on")			{	$seltype = "actr.element";		}
elsif( lxq( "tool.set actr.screen ?") eq "on")			{	$seltype = "actr.screen";		}
elsif( lxq( "tool.set actr.origin ?") eq "on")			{	$seltype = "actr.origin";		}
elsif( lxq( "tool.set actr.parent ?") eq "on")			{	$seltype = "actr.parent";		}
elsif( lxq( "tool.set actr.local ?") eq "on")			{	$seltype = "actr.local";		}
elsif( lxq( "tool.set actr.pivot ?") eq "on")			{	$seltype = "actr.pivot";		}
elsif( lxq( "tool.set actr.pivotparent ?") eq "on")		{	$seltype = "actr.pivotparent";	}

elsif( lxq( "tool.set actr.worldAxis ?") eq "on")		{	$seltype = "actr.worldAxis";	}
elsif( lxq( "tool.set actr.localAxis ?") eq "on")		{	$seltype = "actr.localAxis";	}
elsif( lxq( "tool.set actr.parentAxis ?") eq "on")		{	$seltype = "actr.parentAxis";	}

else
{
	$actr = 0;
	lxout("custom Action Center");
	
	if   ( lxq( "tool.set axis.auto ?") eq "on")		{	 $selAxis = "auto";				}
	elsif( lxq( "tool.set axis.select ?") eq "on")		{	 $selAxis = "select";			}
	elsif( lxq( "tool.set axis.element ?") eq "on")		{	 $selAxis = "element";			}
	elsif( lxq( "tool.set axis.view ?") eq "on")		{	 $selAxis = "view";				}
	elsif( lxq( "tool.set axis.origin ?") eq "on")		{	 $selAxis = "origin";			}
	elsif( lxq( "tool.set axis.parent ?") eq "on")		{	 $selAxis = "parent";			}
	elsif( lxq( "tool.set axis.local ?") eq "on")		{	 $selAxis = "local";			}
	elsif( lxq( "tool.set axis.pivot ?") eq "on")		{	 $selAxis = "pivot";			}
	else												{	 $actr = 1;  $seltype = "actr.auto"; lxout("You were using an action AXIS that I couldn't read");}

	if   ( lxq( "tool.set center.auto ?") eq "on")		{	 $selCenter = "auto";			}
	elsif( lxq( "tool.set center.select ?") eq "on")	{	 $selCenter = "select";			}
	elsif( lxq( "tool.set center.border ?") eq "on")	{	 $selCenter = "border";			}
	elsif( lxq( "tool.set center.element ?") eq "on")	{	 $selCenter = "element";		}
	elsif( lxq( "tool.set center.view ?") eq "on")		{	 $selCenter = "view";			}
	elsif( lxq( "tool.set center.origin ?") eq "on")	{	 $selCenter = "origin";			}
	elsif( lxq( "tool.set center.parent ?") eq "on")	{	 $selCenter = "parent";			}
	elsif( lxq( "tool.set center.local ?") eq "on")		{	 $selCenter = "local";			}
	elsif( lxq( "tool.set center.pivot ?") eq "on")		{	 $selCenter = "pivot";			}
	else												{ 	 $actr = 1;  $seltype = "actr.auto"; lxout("You were using an action CENTER that I couldn't read");}
}
lx("tool.set actr.auto on");


#set the main layer to be "reference" to get the true vert positions.
my $mainlayerID = lxq("query layerservice layer.id ? $mainlayer");
my $layerReference = lxq("layer.setReference ?");
lx("!!layer.setReference $mainlayerID");







#-----------------------------------------------------------------------------------------------------------
#Begin sorting the [edge list] into different [vert rows].
#-----------------------------------------------------------------------------------------------------------
lxmonInit($#origEdgeList_edit/8);
while (($#origEdgeList_edit + 1) != 0)
{
	#this is a loop to go thru and sort the edge loops
	@vertRow = split(/,/, @origEdgeList_edit[0]);
	shift(@origEdgeList_edit);
	&sortRow;

	#take the new edgesort array and add it to the big list of edges.
	push(@vertRowList, "@vertRow");
	if( !lxmonStep ) {	die( "User Abort" );	}
}

#Print out the DONE list   [this should normally go in the sorting sub]
#for ($i = 0; $i < ($#vertRowList + 1) ; $i++) {	lxout("- - -vertRow # ($i) = @vertRowList[$i]"); }




#-----------------------------------------------------------------------------------------------------------
#GO thru each vertRow and COLLAPSE THEM!
#-----------------------------------------------------------------------------------------------------------
lxmonInit($#vertRowList);
foreach my $vertRow (@vertRowList)
{
	my @verts = split (/[^0-9]/, $vertRow);
	my @closestVert1;
	my @closestVert2;
	my @closestVertCenter;

	#find the closest point between the two last edges on this edgeRow
	(@closestVert1[0,1,2],@closestVert2[0,1,2]) = LineLineIntersect(@verts[0],@verts[1],@verts[-2],@verts[-1]);
	@closestVertCenter = (((@closestVert1[0]+@closestVert2[0])*0.5),((@closestVert1[1]+@closestVert2[1])*0.5),((@closestVert1[2]+@closestVert2[2])*0.5));
	#TEMP HACK FIX to fix the unbevel scale problem.
	@closestVertCenter = ((@closestVertCenter[0]/1000),(@closestVertCenter[1]/1000),(@closestVertCenter[2]/1000));
	lxout("closestVertCenter = @closestVertCenter");

	#reselect the verts we want to collapse
	lx("!!select.drop vertex");
	for (my $i=1; $i<$#verts; $i++) {	lx("select.element $mainlayer vertex add @verts[$i]");}

	#collapse them
	lx("tool.set xfrm.scale on");
	lx("tool.reset");
	lx("tool.setAttr center.auto cenX {@closestVertCenter[0]}");
	lx("tool.setAttr center.auto cenY {@closestVertCenter[1]}");
	lx("tool.setAttr center.auto cenZ {@closestVertCenter[2]}");
	lx("tool.setAttr xfrm.scale factor {$scaleAmount}");
	lx("tool.doApply");
	lx("tool.set xfrm.scale off");

	if( !lxmonStep ) {	die( "User Abort" );	}
}



#-----------------------------------------------------------------------------------------------------------
#CLEANUP TIME
#-----------------------------------------------------------------------------------------------------------
#drop selection
my $selected;
lx("select.drop vertex");
lx("select.drop edge");
lx("select.drop polygon");

#vert MERGE
if ($noVertMerge != 1){
	lx("!!vert.merge fixed dist:[1 um]"); #lx("vert.merge dist 1 um");
	lx( "select.drop polygon" );

	#SELECT and delete 0 poly points
	lx("select.vertex add poly equal 0"); #CORRECT way to select o poly points
	$selected = lxq("select.count vertex ?");
	if ($selected != "0"){	lx("delete");	}

	#SELECT 2pt and 1pt polygons and delete 'em
	lx("select.polygon add vertex {$selectPolygonArg} 2");
	lx("select.polygon add vertex {$selectPolygonArg} 1");
	$selected = lxq("select.count polygon ?");
	if ($selected != "0"){	lx("delete");	}

	#SELECT 3+ edge polygons and delete 'em
	lx("select.edge add poly more 2");
	lx("select.convert polygon");
	$selected = lxq("select.count polygon ?");
	if ($selected != "0"){	lx("delete");	}
}

#Put ACTR back
if ($actr == 1) {	lx( "tool.set {$seltype} on" ); }
else { lx("tool.set center.$selCenter on"); lx("tool.set axis.$selAxis on"); }

#Set the symmetry mode back
if ($symmAxis != 3)
{
	#CONVERT MY OLDSCHOOL SYMM AXIS TO MODO's NEWSCHOOL NAME
	if 		($symmAxis == "3")	{	$symmAxis = "none";	}
	elsif	($symmAxis == "0")	{	$symmAxis = "x";		}
	elsif	($symmAxis == "1")	{	$symmAxis = "y";		}
	elsif	($symmAxis == "2")	{	$symmAxis = "z";		}
	lxout("turning symm back on ($symmAxis)"); lx("!!select.symmetryState $symmAxis");
}


#Set the layer reference back
lx("!!layer.setReference [$layerReference]");

#Put workplane back
lx("workPlane.edit {@WPmem[0]} {@WPmem[1]} {@WPmem[2]} {@WPmem[3]} {@WPmem[4]} {@WPmem[5]}");

#set the selection mode back to EDGE
if ($noVertMerge != 1)	{	lx("select.drop edge");	}

#restore selection in hack way if just resizing bevel and not unbeveling.
if ($scaleAmount != 0){
	foreach my $edge (@origEdgeList){
		my @verts = split (/[^0-9]/, $edge);
		lx("!!select.element $mainlayer edge add $verts[0] $verts[1]");
	}
}















#***********************************************************************************
#***********************************************************************************
#******************                   SUBROUTINES         *******************************
#***********************************************************************************
#***********************************************************************************

#-----------------------------------------------------------------------------------------------------------
#sort Rows subroutine
#-----------------------------------------------------------------------------------------------------------
sub sortRow
{
	#this first part is stupid.  I need it to loop thru one more time than it will:
	my @loopCount = @origEdgeList_edit;
	unshift (@loopCount,1);
	#lxout("How many fucking times will I go thru the loop!? = $#loopCount");

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




#-----------------------------------------------------------------------------------------------------------
#Find the closest point between two vectors subroutine
#-----------------------------------------------------------------------------------------------------------
sub LineLineIntersect #This subroutine will find the closest point between 2 vectors (stolen from Chris Johnson's max script, whom got the knowledge from Paul Bourke)
{
	#lxout("[->] Using LineLineIntersect subroutine");

	my ($p1,$p2,$p3,$p4) = @_;
	my @p1Pos = lxq("query layerservice vert.pos ? $p1");
	my @p2Pos = lxq("query layerservice vert.pos ? $p2");
	my @p3Pos = lxq("query layerservice vert.pos ? $p3");
	my @p4Pos = lxq("query layerservice vert.pos ? $p4");
	#lxout("p1Pos=@p1Pos<>p2Pos=@p2Pos<>p3Pos=@p3Pos<>p4Pos=@p4Pos");

	#TEMP HACK FIX to fix the unbevel scale problem.
	@p1Pos = ((@p1Pos[0]*1000),(@p1Pos[1]*1000),(@p1Pos[2]*1000));
	@p2Pos = ((@p2Pos[0]*1000),(@p2Pos[1]*1000),(@p2Pos[2]*1000));
	@p3Pos = ((@p3Pos[0]*1000),(@p3Pos[1]*1000),(@p3Pos[2]*1000));
	@p4Pos = ((@p4Pos[0]*1000),(@p4Pos[1]*1000),(@p4Pos[2]*1000));

	my $EPS = 0.000002;
	#lxout("EPS=$EPS");

	my @p13 = ((@p1Pos[0] - @p3Pos[0]),(@p1Pos[1] - @p3Pos[1]),(@p1Pos[2] - @p3Pos[2]));
	my @p43 = ((@p4Pos[0] - @p3Pos[0]),(@p4Pos[1] - @p3Pos[1]),(@p4Pos[2] - @p3Pos[2]));
	#lxout("p13=@p13");
	#lxout("p43=@p43");

	if ( (abs(@p43[0]) < $EPS) && (abs(@p43[1]) < $EPS) && (abs(@p43[2]) < $EPS) ) {popup("less than?  huh?"); return;}

	my @p21 = ((@p2Pos[0] - @p1Pos[0]),(@p2Pos[1] - @p1Pos[1]),(@p2Pos[2] - @p1Pos[2]));
	#lxout("p21=@p21	");

	if ( (abs(@p21[0]) < $EPS) && (abs(@p21[1]) < $EPS) && (abs(@p21[2]) < $EPS) ) {popup("less than?  huh?"); return;}

	my $d1343 = @p13[0] * @p43[0] + @p13[1] * @p43[1] + @p13[2] * @p43[2];
	my $d4321 = @p43[0] * @p21[0] + @p43[1] * @p21[1] + @p43[2] * @p21[2];
	my $d1321 = @p13[0] * @p21[0] + @p13[1] * @p21[1] + @p13[2] * @p21[2];
	my $d4343 = @p43[0] * @p43[0] + @p43[1] * @p43[1] + @p43[2] * @p43[2];
	my $d2121 = @p21[0] * @p21[0] + @p21[1] * @p21[1] + @p21[2] * @p21[2];
	#lxout("d1343=$d1343");
	#lxout("d4321=$d4321");
	#lxout("d1321=$d1321");
	#lxout("d4343=$d4343");
	#lxout("d2121=$d2121");

	my $denom = ($d2121 * $d4343 - $d4321 * $d4321);
	#lxout("denom = $denom ");
	if (abs($denom) < $EPS) {popup("less than?"); return;}


	my $numer = ($d1343 * $d4321 - $d1321 * $d4343);

	my $mua = $numer / $denom;
	my $mub = ($d1343 + ($d4321 * $mua)) / $d4343;

	#lxout("mua = $mua");
	#lxout("mub = $mub");

	my @pa = ((@p1Pos[0] + (@p21[0]*$mua)),(@p1Pos[1] + (@p21[1]*$mua)),(@p1Pos[2] + (@p21[2]*$mua)));
	my @pb = ((@p3Pos[0] + (@p43[0]*$mub)),(@p3Pos[1] + (@p43[1]*$mub)),(@p3Pos[2] + (@p43[2]*$mub)));
	#lxout("pa=@pa");
	#lxout("pb=@pb");

	return (@pa,@pb);
}


#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#QUICK DIALOG SUB v2.1
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#USAGE : quickDialog(username,float,initialValue,min,max);
sub quickDialog{
	if (@_[1] eq "yesNo"){
		lx("dialog.setup yesNo");
		lx("dialog.msg {$_[0]}");
		lx("dialog.open");
		if (lxres != 0){	die("The user hit the cancel button");	}
		return (lxq("dialog.result ?"));
	}else{
		if (lxq("query scriptsysservice userValue.isdefined ? seneTempDialog") == 1){
			lx("user.defDelete seneTempDialog");
		}
		lx("user.defNew name:[seneTempDialog] type:{$_[1]} life:[momentary]");		
		lx("user.def seneTempDialog username [$_[0]]");
		if (($_[3] != "") && ($_[4] != "")){
			lx("user.def seneTempDialog min [$_[3]]");
			lx("user.def seneTempDialog max [$_[4]]");
		}
		lx("user.value seneTempDialog [$_[2]]");
		lx("user.value seneTempDialog ?");
		if (lxres != 0){	die("The user hit the cancel button");	}
		return(lxq("user.value seneTempDialog ?"));
	}
}

#-----------------------------------------------------------------------------------------------------------
#popup subroutine
#-----------------------------------------------------------------------------------------------------------
sub popup #(MODO2 FIX)
{
	lx("dialog.setup yesNo");
	lx("dialog.msg {@_}");
	lx("dialog.open");
	my $confirm = lxq("dialog.result ?");
	if($confirm eq "no"){die;}
}

