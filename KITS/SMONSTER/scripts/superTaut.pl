#perl
#BY: Seneca Menard
#version 3.2
#(8-14-05 overhaul) This script is for straightening out VERTS or EDGES to any angle you define.
#(8-8-06) supertaut works now on moved items, but constrained tauts don't.  :(
#(11-14-06) : I reorder the layer reference command to hide modo's workplane flip bug.
#(12-15-06 bugfix) : I put in the code to fix the element actr so your tools won't freak out anymore when you turn them on after running this script.  :)
#(12-15-06 bugfix) : I noticed there was a typo with the vert mode and symmetry
#(12-15-06 feature) : I'm now restoring selections after the script is done.
#(12-18-08 fix) : I went and removed the square brackets so that the numbers will always be read as metric units and also because my prior safety check would leave the unit system set to metric system if the script was canceled because changing that preference doesn't get undone if a script is cancelled.
#(1-10-14 fix) : got the actr storage system up to date with 601

#VERT MODE instructions: First select the two points that define the angle, and then select the points you want to move:
#EDGE MODE instructions: You can do two things with edges.  You can select a whole bunch of edgerows, and it will TAUT each edgerow by it's own endpoints, OR you
#can select one single edge and then select a whole bunch of other edges, and it will TAUT ALL of those edges to the first selected edge's angle.

# There are also a number of different types of TAUTS you can run:
#- 3Dlinear : This will take the selected elements and make them into straight 3D line(s).
#- 2Dlinear: This will take the selected elements and make them into straight 2D line(s), and the 3rd dimension won't be touched
#- Axis Constrained 2Dlinear:  This will do a 2dlinear taut, but only move the verts horizontally or vertically
#- Also, you can run this script in any symmetry modes now and it all works perfectly.  :)




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#SETUP
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
my $mainlayer = lxq("query layerservice layers ? main");
our $ratioValue;
our $missingAxis;
our $axis;
our $direction;
our $linearX;
our $linearY;
our $linearZ;
our @linearAxisFlip;
our @disp;
our $vertRowOverride = 0;
our $selectMode = "vert";

#-----------------------------------------------------------------------------------
#SAFETY CHECKS
#-----------------------------------------------------------------------------------
#Remember what the workplane was and turn it off
my @WPmem;
@WPmem[0] = lxq ("workPlane.edit cenX:? ");
@WPmem[1] = lxq ("workPlane.edit cenY:? ");
@WPmem[2] = lxq ("workPlane.edit cenZ:? ");
@WPmem[3] = lxq ("workPlane.edit rotX:? ");
@WPmem[4] = lxq ("workPlane.edit rotY:? ");
@WPmem[5] = lxq ("workPlane.edit rotZ:? ");
lx("workPlane.reset ");

#CONVERT THE SYMM AXIS TO MY OLDSCHOOL NUMBER AND TURN SYMM OFF.
our $symmAxis = lxq("select.symmetryState ?");
if 		($symmAxis eq "none")	{	$symmAxis = 3;	}
elsif	($symmAxis eq "x")		{	$symmAxis = 0;	}
elsif	($symmAxis eq "y")		{	$symmAxis = 1;	}
elsif	($symmAxis eq "z")		{	$symmAxis = 2;	}
if ($symmAxis != 3) 				{lx("select.symmetryState none");}


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
lx("tool.set actr.selectauto on");

#set the main layer to be "reference" to get the true vert positions.
my $mainlayerID = lxq("query layerservice layer.id ? $mainlayer");
my $layerReference = lxq("layer.setReference ?");
lx("!!layer.setReference $mainlayerID");



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#WHAT TO DO IF IN VERT MODE
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
if( lxq( "select.typeFrom {vertex;edge;polygon;item} ?" ) )
{
	lxout("[->] VERT MODE");
	lx("select.editSet senetemp add");
	our @vertSel = lxq("query layerservice verts ? selected");
	our @backupVerts = @vertSel;

	# IF SYMM IS OFF
	if ($symmAxis == 3)
	{
		lxout("[->] SYMMETRY IS OFF");
		&vertMode;
	}

	# IF SYMM IS ON
	else
	{
		lxout("[->] SYMMETRY IS ON");
		our $allVertsOnAxis =1;  #this is to make sure not to run the script twice if all the verts are ON the axis.
		our @vertListPos;
		our @vertListNeg;
		my $count = 0;


		#-----------------------------------------------------------------------------------------
		#CHECK WHICH VERTS ARE ON WHICH SIDE OF THE AXIS
		#-----------------------------------------------------------------------------------------
		foreach my $vert (@vertSel)
		{
			#POSITIVE check
			my @vertPos = lxq("query layerservice vert.pos ? $vert");
			#lxout("vert[$vert]Pos = @vertPos");
			if (@vertPos[$symmAxis] > 0.00000001)
			{
				#lxout("[$count] = (vert$vert)POS");
				push(@vertListPos, "$vert");
				$allVertsOnAxis =0;
			}
			#NEGATIVE check
			elsif (@vertPos[$symmAxis] < -0.00000001)
			{
				#lxout("[$count] = (vert$vert)NEG");
				push(@vertListNeg, "$vert");
				$allVertsOnAxis =0;
			}
			#THEN THIS VERT MUST BE ON THE AXIS
			else
			{
				#lxout("[$count] = (vert$vert)ON AXIS!");
				push(@vertListPos, "$vert");
				push(@vertListNeg, "$vert");
			}
			$count++;
		}


		#-----------------------------------------------------------------------------------------
		#NOW RUN THE SCRIPT ON EACH HALF OF THE MODEL
		#-----------------------------------------------------------------------------------------

		#all verts on 0 message
		if ($allVertsOnAxis == 1)	{lxout("[->] ALL the verts are ON the symm axis, so i'm not using symmetry");}

		#POSITIVE (check to make sure it should be running the script on the positive half)
		if ($#vertListPos > 1)
		{
			@vertSel = @vertListPos;

			#select the POSITIVE HALF
			lx("select.drop vertex");
			foreach my $vert (@vertSel)	{	lx("select.element [$mainlayer] vertex add index:$vert]");	}

			&vertMode;
		}

		#NEGATIVE (check to make sure it should be running the script on the positive half)
		if (($#vertListNeg > 1) && ($allVertsOnAxis == 0))
		{
			@vertSel = @vertListNeg;

			#select the NEGATIVE HALF
			lx("select.drop vertex");
			foreach my $vert (@vertSel)	{	lx("select.element [$mainlayer] vertex add index:$vert]");	}

			&vertMode;
		}
	}
}



#-----------------------------------------------------------------------------------------
#VERT MODE COMMANDS
#-----------------------------------------------------------------------------------------
sub vertMode()
{
	#define the angle Edge Vector
	our @firstVertPos = lxq("query layerservice vert.pos ? @vertSel[0]");
	our @secondVertPos = lxq("query layerservice vert.pos ? @vertSel[1]");
	our @angleEdgeVector = ((@secondVertPos[0] - @firstVertPos[0]),(@secondVertPos[1] - @firstVertPos[1]),(@secondVertPos[2] - @firstVertPos[2]));

	#remove the two (TAUT-ANGLE-defining VERTS) from the original selection
	our @prunedVertSel = @vertSel;
	shift(@prunedVertSel);
	shift(@prunedVertSel);

	#SCRIPT-USE DECISIONS
	foreach $arg(@ARGV)
	{
		if ($arg eq "X")			{	$linearX=1;		&linear_2D;				}
		if ($arg eq "Y")			{	$linearY=1;		&linear_2D;				}
		if ($arg eq "Z")			{	$linearZ=1;		&linear_2D;				}
		if ($arg eq "2Dconst")		{	$constr2D=1; 	&constrained_2D;		}
		if ($arg eq "3Dline")		{	&linear_3D;								}
	}
}


#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#WHAT TO DO IF IN EDGE MODE
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
if( lxq( "select.typeFrom {edge;polygon;item;vertex} ?" ) )
{
	lxout("[->] EDGE MODE");
	lx("select.editSet senetemp add");
	$selectMode = "edge";
	my $count = 0;

	#Get and edit the original edge list *throw away all edges that aren't in mainlayer* (FIXED FOR MODO2)
	our @origEdgeList = lxq("query layerservice selection ? edge");
	my @tempEdgeList;
	foreach my $edge (@origEdgeList){	if ($edge =~ /\($mainlayer/){	push(@tempEdgeList,$edge);		}	}
	#[remove layer info] [remove ( ) ]
	@origEdgeList = @tempEdgeList;
	s/\(\d{0,},/\(/  for @origEdgeList;
	tr/()//d for @origEdgeList;
	our @backupEdges = @origEdgeList;

	# IF SYMM IS OFF
	if ($symmAxis == 3)
	{
		lxout("[->] SYMMETRY IS OFF");
		&edgeMode;
	}

	# IF SYMM IS ON
	else
	{
		lxout("[->] SYMMETRY IS ON");
		our $allVertsOnAxis =1;
		our @edgeListPos;
		our @edgeLisNeg;


		#CHECK WHICH EDGES ARE ON WHICH SIDE OF THE AXIS
		foreach my $edge (@origEdgeList)
		{
			my @verts = split(/,/, $edge);
			#lxout("[$count]:verts = @verts");

			#TIME TO CHECK VERT0---------------------------------
			#vert0 POSITIVE check
			my @vert0Pos = lxq("query layerservice vert.pos ? @verts[0]");
			#lxout("--[@verts[0]]vert0Pos = @vert0Pos");
			if (@vert0Pos[$symmAxis] > 0.00000001)
			{
				#lxout("[$count]0 = POS");
				push(@edgeListPos, "$edge");
				$allVertsOnAxis =0;
			}
			#vert0 NEGATIVE check
			elsif (@vert0Pos[$symmAxis] < -0.00000001)
			{
				#lxout("[$count]0 = NEG");
				push(@edgeListNeg, "$edge");
				$allVertsOnAxis =0;
			}

			#TIME TO CHECK VERT1---------------------------------
			else
			{
				#vert1 POSITIVE check
				my @vert1Pos = lxq("query layerservice vert.pos ? @verts[1]");
				#lxout("--[@verts[1]]vert1Pos = @vert1Pos");
				if (@vert1Pos[$symmAxis] > 0.00000001)
				{
					#lxout("[$count]1 = POS");
					push(@edgeListPos, "$edge");
					$allVertsOnAxis =0;
				}
				#vert1 NEGATIVE check
				elsif (@vert1Pos[$symmAxis] < -0.00000001)
				{
					#lxout("[$count]1 = NEG");
					push(@edgeListNeg, "$edge");
					$allVertsOnAxis =0;
				}

				#I guess both verts are on ZERO then.
				else
				{
					#lxout("[$count]NEITHER");
					push(@edgeListPos, "$edge");
					push(@edgeListNeg, "$edge");
				}
			}
			$count++;
		}


		#-----------------------------------------------------------------------------------------
		#NOW RUN THE SCRIPT ON EACH HALF OF THE MODEL
		#-----------------------------------------------------------------------------------------

		#all verts on 0 message
		if ($allVertsOnAxis == 1)	{lxout("[->] ALL the verts are ON the symm axis, so i'm not using symmetry");}

		#POSITIVE (check to make sure it should be running the script on the positive half)
		if ($#edgeListPos > 0)
		{
			#grab the POS edges
			@origEdgeList = @edgeListPos;

			#select the POSITIVE HALF
			lx("select.drop edge");
			foreach my $edge (@origEdgeList)
			{
				my @verts = split (/[^0-9]/, $edge);
				lx("select.element $mainlayer edge add @verts[0] @verts[1]");
			}
			&edgeMode;
		}
		else	{	lxout("[->] NOT RUNNING script on POS half");	}

		#NEGATIVE (check to make sure it should be running the script on the negative half)
		if (($#edgeListNeg > 0) && ($allVertsOnAxis == 0))
		{
			#grab the POS edges
			@origEdgeList = @edgeListNeg;

			#select the NEGATIVE HALF
			lx("select.drop edge");
			foreach my $edge (@origEdgeList)
			{
				my @verts = split (/[^0-9]/, $edge);
				lx("select.element $mainlayer edge add @verts[0] @verts[1]");
			}
			&edgeMode;
		}
		else	{	lxout("[->] NOT RUNNING script on NEG half");	}
	}
}



#-----------------------------------------------------------------------------------------
#EDGE MODE COMMANDS
#-----------------------------------------------------------------------------------------
sub edgeMode()
{
	our @origEdgeList_edit = @origEdgeList;
	our @vertRow;
	our @vertRowList;
	undef(@vertRowList);

	our @vertList;
	our %vertPosTable;
	our %endPointVectors;

	our @vertMergeOrder;
	our @edgesToRemove;
	our $removeEdges = 0;


	#-----------------------------------------------------------------------------------------------------------
	#Begin sorting the [edge list] into different [vert rows].
	#-----------------------------------------------------------------------------------------------------------
	while (($#origEdgeList_edit + 1) != 0)
	{
		#this is a loop to go thru and sort the edge loops
		@vertRow = split(/,/, @origEdgeList_edit[0]);
		shift(@origEdgeList_edit);
		&sortRow;

		#take the new edgesort array and add it to the big list of edges.
		push(@vertRowList, "@vertRow");
	}


	#-----------------------------------------------------------------------------------------------------------
	#If any of the VERTROWS only have ONE EDGE, it'll merge all of the [vertrows] into one.
	#-----------------------------------------------------------------------------------------------------------
	my @vertCount = split (/[^0-9]/, @vertRowList[0]);
	if ($#vertCount == 1)
	{
		lxout("[->] I'm overriding the selected edgerows, because edgeRow1 has two verts");
		$vertRowOverride = 1;

		my $newVertRowList = @vertCount[0] . " " . @vertCount[1];

		for ($i = 1; $i < ($#vertRowList + 1) ; $i++)
		{
			$newVertRowList = $newVertRowList . " " . @vertRowList[$i];
			#lxout("newVertRowList = $newVertRowList");
		}
		@vertRowList = $newVertRowList;
	}



	#-----------------------------------------------------------------------------------------------------------
	#Print out the DONE list   [this should normally go in the sorting sub]
	#-----------------------------------------------------------------------------------------------------------
	#lxout("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");
	#lxout("- - -This is the new vertRow: @vertRow");
	#lxout("- - -DONE: There are ($#vertRowList+1) edge rows total");
	#for ($i = 0; $i < ($#vertRowList + 1) ; $i++) {	lxout("- - -vertRow # ($i) = @vertRowList[$i]"); }
	#lxout("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - ");


	#-----------------------------------------------------------------------------------------------------------
	#LOOP THRU AND DO THE MULTIPLE TAUTS
	#-----------------------------------------------------------------------------------------------------------
	for ($i = 0; $i < ($#vertRowList + 1) ; $i++)
	{

		#clean up the edge selection and convert to verts (BUT ONLY IF WE'RE NOT MERGING THE VERTROWS)
		if ($vertRowOverride == 0)
		{
			our @vertSel = split (/[^0-9]/, @vertRowList[$i]);
			my $temp = splice(@vertSel, -1,1);
			splice(@vertSel, 1,0, $temp);  #(add/delete from anwyhere in the array)  #id1=arrayname <> id2=which element <> id3=delete how many elements <> id4=add these at that element#
			our @prunedVertSel = @vertSel;
		}
		else
		{
			our @vertSel = split (/[^0-9]/, @vertRowList[0]);
			our @prunedVertSel = @vertSel;
		}


		#SELECT THE VERTS
		lx("select.drop vertex");
		foreach my $vert (@vertSel)
		{
			lx("select.element [$mainlayer] vertex add $vert");
		}


		#define the angle Edge Vector
		our @firstVertPos = lxq("query layerservice vert.pos ? @vertSel[0]");
		our @secondVertPos = lxq("query layerservice vert.pos ? @vertSel[1]");
		our @angleEdgeVector = ((@secondVertPos[0] - @firstVertPos[0]),(@secondVertPos[1] - @firstVertPos[1]),(@secondVertPos[2] - @firstVertPos[2]));

		#make sure at least 3 verts are selected
		if (lxq("select.count vertex ?") < 3)
		{
			die("\n.\n[---------------------------------------------You need to have at least 3 verts selected--------------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}

		#-----------------------------------------------------------------------------------
		#SCRIPT-USE DECISIONS
		#-----------------------------------------------------------------------------------

		foreach $arg(@ARGV)
		{
			if ($arg eq "X")			{	$linearX=1;	&linear_2D;				}
			if ($arg eq "Y")			{	$linearY=1;	&linear_2D;				}
			if ($arg eq "Z")			{	$linearZ=1;	&linear_2D;				}
			if ($arg eq "2Dconst")		{	$constr2D=1; &constrained_2D;		}
			if ($arg eq "3Dline")		{	&linear_3D;							}
		}
	}
}







#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------2d AXIS CONSTRAINED TAUT-------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------
#CHECK SCRIPT ARGUMENTS to pick axis and direction
#-----------------------------------------------------------------------------------
sub constrained_2D
{
	foreach $arg(@ARGV)
	{
		if ($arg eq "X")	{	$axis = X;	}
		if ($arg eq "Y")	{	$axis = Y;	}
		if ($arg eq "Z")	{	$axis = Z;	}
		if ($arg eq "H")	{	$direction = H;	}
		if ($arg eq "V")	{	$direction = V;	}
	}

	#CHECK which axes and then send to move sub
	if ($axis eq X)
	{
		if ($direction eq V)
		{
			#lxout("Picked Vertical direction on X axis");
			$ratioValue = (@angleEdgeVector[1]/@angleEdgeVector[2]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		elsif ($direction eq H)
		{
			#lxout("Picked Horizontal direction on X axis");
			$ratioValue = (@angleEdgeVector[2]/@angleEdgeVector[1]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		else
		{
			die("\n.\n[---------------------------------------------------Script can't run without a direction------------------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}
	}
	elsif ($axis eq Y)
	{
		if ($direction eq V)
		{
			#lxout("Picked Vertical direction on Y axis");
			$ratioValue = (@angleEdgeVector[2]/@angleEdgeVector[0]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		elsif ($direction eq H)
		{
			#lxout("Picked Horizontal direction on Y axis");
			$ratioValue = (@angleEdgeVector[0]/@angleEdgeVector[2]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		else
		{
			die("\n.\n[---------------------------------------------------Script can't run without a direction------------------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}
	}
	elsif ($axis eq Z)
	{
		if ($direction eq V)
		{
			#lxout("Picked Vertical direction on Z axis");
			#lxout("ratioValue = (@angleEdgeVector[1]/@angleEdgeVector[0]);");
			$ratioValue = (@angleEdgeVector[1]/@angleEdgeVector[0]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		elsif ($direction eq H)
		{
			#lxout("Picked Horizontal direction on Z axis");
			$ratioValue = (@angleEdgeVector[0]/@angleEdgeVector[1]);
			#lxout("ratioValue = $ratioValue ");
			&planarMove;
		}
		else
		{
			die("\n.\n[---------------------------------------------------Script can't run without a direction------------------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}
	}
	else
	{
		die("\n.\n[--------------------------------------------Script can't run without an axis and a direction-----------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
	}
}



#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------2D LINEAR TAUT---------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
sub linear_2D
{
	#this IF check is really stupid.   It's to skip past this subroutine if 2dlinear is being used.  It shouldn't even be here.
	if ($constr2D != 1)
	{
		#this will fake that the vector is aligned to the origin.
		if ($linearX == 1)
		{
			#lxout("faking X");
			@secondVertPos[0] = @firstVertPos[0]
		}
		elsif ($linearY == 1)
		{
			#lxout("faking Y");
			@secondVertPos[1] = @firstVertPos[1]
		}
		elsif ($linearZ == 1)
		{
			#lxout("faking Z");
			@secondVertPos[2] = @firstVertPos[2]
		}

		#get the fake axis aligned disp.
		@disp[0,1,2] = (@secondVertPos[0]-@firstVertPos[0],@secondVertPos[1]-@firstVertPos[1],@secondVertPos[2]-@firstVertPos[2]);
		my $dist = sqrt((@disp[0]*@disp[0])+(@disp[1]*@disp[1])+(@disp[2]*@disp[2]));

		#normalize displacement vector and then turn it into a percentage
		@disp[0,1,2] = ((@disp[0]/$dist)*100,(@disp[1]/$dist)*100,(@disp[2]/$dist)*100);
		#lxout("2d linear disp vector= @disp[0] <><> @disp[1] <><> @disp[2]");

		#do the axis.element flips for the different axes
		if ($linearX == 1)
		{
			@linearAxisFlip[0] = @disp[0];
			@linearAxisFlip[1] = @disp[2];
			@linearAxisFlip[2] = (@disp[1]*-1);
		}
		elsif ($linearY == 1)
		{
			@linearAxisFlip[0] = @disp[2];
			@linearAxisFlip[1] = @disp[1];
			@linearAxisFlip[2] = (@disp[0]*-1);
		}
		elsif ($linearZ == 1)
		{
			@linearAxisFlip[0] = @disp[1];
			@linearAxisFlip[1] = (@disp[0]*-1);
			@linearAxisFlip[2] = @disp[2];
		}

		#lxout("2d linear axis flip= @linearAxisFlip[0] <><> @linearAxisFlip[1] <><> @linearAxisFlip[2]");

		#STRETCH TOOL
		#must switch to element mode
		lx("tool.set actr.element on");

		lx("tool.set xfrm.stretch on");
		lx("tool.reset");
		lx("tool.setAttr center.element cenX {@firstVertPos[0]}");
		lx("tool.setAttr center.element cenY {@firstVertPos[1]}");
		lx("tool.setAttr center.element cenZ {@firstVertPos[2]}");
		lx("tool.setAttr axis.element axisX {@linearAxisFlip[0]}");
		lx("tool.setAttr axis.element axisY {@linearAxisFlip[1]}");
		lx("tool.setAttr axis.element axisZ {@linearAxisFlip[2]}");
		lx("tool.setAttr axis.element axis {-1}");
		lx("tool.setAttr axis.element upX {@disp[0]}");
		lx("tool.setAttr axis.element upY {@disp[1]}");
		lx("tool.setAttr axis.element upZ {@disp[2]}");
		lx("tool.setAttr xfrm.stretch factX {1}");
		lx("tool.setAttr xfrm.stretch factY {1}");
		lx("tool.setAttr xfrm.stretch factZ {0}");
		lx("tool.doApply");
		lx("tool.set xfrm.stretch off");
	}
}




#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------3D LINEAR TAUT---------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------------------------------------------------------------------------------------------------------
sub linear_3D
{
	#finding the angle of the 2 selected points.
	my @XYZ_dotProduct = axisDotProduct();
	@XYZ_dotProduct = (@XYZ_dotProduct[0]*100,@XYZ_dotProduct[1]*100,@XYZ_dotProduct[2]*100);

	#find the other two tool handle axes with a crossproduct check
	my @crossProducts = twoVertCPSetup(\@secondVertPos,\@firstVertPos);
	my @axis = (@crossProducts[0]*100 , @crossProducts[1]*100 , @crossProducts[2]*100);

	#finding the center of the 2 selected points
	my @tautCenter = (((@firstVertPos[0]+@secondVertPos[0]) / 2) , ((@firstVertPos[1]+@secondVertPos[1]) / 2) , ((@firstVertPos[2]+@secondVertPos[2]) / 2));

	#STRETCH TOOL
	#must switch to element mode
	lx("tool.set actr.element on");

	lx("tool.set xfrm.stretch on");
	lx("tool.reset");
	lx("tool.setAttr center.element cenX {@tautCenter[0]}");
	lx("tool.setAttr center.element cenY {@tautCenter[1]}");
	lx("tool.setAttr center.element cenZ {@tautCenter[2]}");
	lx("tool.setAttr axis.element axisX {@axis[0]}");
	lx("tool.setAttr axis.element axisY {@axis[1]}");
	lx("tool.setAttr axis.element axisZ {@axis[2]}");
	lx("tool.setAttr axis.element axis {-1}");
	lx("tool.setAttr axis.element upX {@XYZ_dotProduct[0]}");
	lx("tool.setAttr axis.element upY {@XYZ_dotProduct[1]}");
	lx("tool.setAttr axis.element upZ {@XYZ_dotProduct[2]}");
	lx("tool.setAttr xfrm.stretch factX {0}");
	lx("tool.setAttr xfrm.stretch factY {1}");
	lx("tool.setAttr xfrm.stretch factZ {0}");
	lx("tool.doApply");
	lx("tool.set xfrm.stretch off");
}






#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#--------------------------------------------SUBROUTINES---------------------------------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------
#CROSSPRODUCT FROM 1 VECTOR (in=2pos out=2vec)
#-------------------------------------------------------------------------
sub twoVertCPSetup{
	my $pos1 = @_[0];
	my $pos2 = @_[1];

	my @pos1 = @$pos1;
	my @pos2 = @$pos2;

	#create the real vector
	my @vector1 = ((@pos2[0]-@pos1[0]),(@pos2[1]-@pos1[1]),(@pos2[2]-@pos1[2]));
	@vector1 = unitVector(@vector1);

	#create the fake vector
	my @vector2 = (0,1,0);
	my $dp = (@vector1[0]*@vector2[0] + @vector1[1]*@vector2[1] + @vector1[2]*@vector2[2]);
	if (abs($dp) > .95){	@vector2 = (1,0,0);	}

	#create the first and second crossProduct
	my @crossProduct = crossProduct(\@vector1,\@vector2);
	@crossProduct = unitVector(@crossProduct);
	my @secondCrossProduct = crossProduct(\@vector1,\@crossProduct);

	return(@crossProduct,@secondCrossProduct);
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

#-------------------------------------------------------------------------
#UNIT VECTOR SUBROUTINE
#-------------------------------------------------------------------------
sub unitVector{
	my $dist1 = sqrt((@_[0]*@_[0])+(@_[1]*@_[1])+(@_[2]*@_[2]));
	@_ = ((@_[0]/$dist1),(@_[1]/$dist1),(@_[2]/$dist1));
	return @_;
}

#-----------------------------------------------------------------------------------
#PLANAR MOVE (2d constrained move)
#-----------------------------------------------------------------------------------
sub planarMove
{
	#lxout("prunedVertSel = @prunedVertSel"); #temp
	#run thru each vert and put it in the proper position
	foreach my $prunedVert(@prunedVertSel)
	{
		my @pos = lxq("query layerservice vert.pos ? $prunedVert");
		#lxout("pos = @pos");

		#select and move
		lx("select.drop vertex");
		lx("select.element [$mainlayer] vertex add index:$prunedVert");
		if ($axis eq Z)
		{
			if ($direction eq V)
			{
				$missingAxis = ((@pos[0]-@firstVertPos[0])*($ratioValue)+@firstVertPos[1]);
				#lxout("V MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				lx("vert.set y {$missingAxis}");
			}
			elsif ($direction eq H)
			{
				#lxout("H MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				$missingAxis = ((@pos[1]-@firstVertPos[1])*($ratioValue)+@firstVertPos[0]);
				lx("vert.set x {$missingAxis}");
			}
		}
		elsif ($axis eq X)
		{
			if ($direction eq V)
			{
				$missingAxis = ((@pos[2]-@firstVertPos[2])*($ratioValue)+@firstVertPos[1]);
				#lxout("V MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				lx("vert.set y {$missingAxis}");
			}
			elsif ($direction eq H)
			{
				#lxout("H MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				$missingAxis = ((@pos[1]-@firstVertPos[1])*($ratioValue)+@firstVertPos[2]);
				lx("vert.set z {$missingAxis}");
			}
		}
		elsif ($axis eq Y)
		{
			if ($direction eq V)
			{
				$missingAxis = ((@pos[0]-@firstVertPos[0])*($ratioValue)+@firstVertPos[2]);
				#lxout("V MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				lx("vert.set z {$missingAxis}");
			}
			elsif ($direction eq H)
			{
				#lxout("H MOVING <> vert = $prunedVert <><> pos = @pos <><> missing axis = $missingAxis");
				$missingAxis = ((@pos[2]-@firstVertPos[2])*($ratioValue)+@firstVertPos[0]);
				lx("vert.set x {$missingAxis}");
			}
		}
		else
		{
			die("\n.\n[--------------------------------------------Script can't run without an axis and a direction-----------------------------------------]\n[--PLEASE TURN OFF THIS WARNING WINDOW by clicking on the (In the future) button and choose (Hide Message)--] \n[-----------------------------------This window is not supposed to come up, but I can't control that.---------------------------]\n.\n");
		}
	}
}





#-----------------------------------------------------------------------------------
#AXIS DOT-PRODUCT (angle check)
#-----------------------------------------------------------------------------------
sub axisDotProduct
{
	#distance check
	@disp[0,1,2] = (@secondVertPos[0]-@firstVertPos[0],@secondVertPos[1]-@firstVertPos[1],@secondVertPos[2]-@firstVertPos[2]);
	my $dist = sqrt((@disp[0]*@disp[0])+(@disp[1]*@disp[1])+(@disp[2]*@disp[2]));

	#normalize displacement vector (but first get rid of ZEROs)
	#if (@disp[0] == 0)	{ @disp[0] = 0.00000001;	}
	#if (@disp[1] == 0)	{ @disp[1] = 0.00000001;	}
	#if (@disp[2] == 0)	{ @disp[2] = 0.00000001;	}
	@disp[0,1,2] = (@disp[0]/$dist,@disp[1]/$dist,@disp[2]/$dist);
	return @disp;
}




#-----------------------------------------------------------------------------------
#ANGLE CHECK (modified from original because disp already exists.)
#-----------------------------------------------------------------------------------
sub anglecheck
{
	my $radian;
	my $pi = 3.1415926535897932384626433832795;

	my ($angle1,$angle2) = @_;
	$radian = atan2(@angleEdgeVector[$angle1],@angleEdgeVector[$angle2]);
	my $angle = ($radian*180)/$pi;
	#lxout("angle1 = $angle1<> angle2 = $angle2 <> true angle = $angle");
	return $angle;
}


#-----------------------------------------------------------------------------------
#SORT ROWS subroutine
#-----------------------------------------------------------------------------------
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


#-----------------------------------------------------------------------------------
#POPUP WINDOW subroutine
#-----------------------------------------------------------------------------------
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
#------------[SCRIPT IS FINISHED] SAFETY REIMPLEMENTING-----------------
#------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------
#Put original selection back
if ($selectMode eq "edge")	{	lx("select.drop edge");	}
else						{	lx("select.drop vertex");	}
lx("select.useSet senetemp select");
lx("select.editSet senetemp remove");

#Set the action center settings back
if ($actr == 1) {	lx( "tool.set {$seltype} on" ); }
else { lx("tool.set center.$selCenter on"); lx("tool.set axis.$selAxis on");}

#Set the layer reference back
lx("!!layer.setReference [$layerReference]");

#Put the workplane back
lx("workPlane.edit {@WPmem[0]} {@WPmem[1]} {@WPmem[2]} {@WPmem[3]} {@WPmem[4]} {@WPmem[5]}");

#Set Symmetry back
if ($symmAxis != 3)
{
	#CONVERT MY OLDSCHOOL SYMM AXIS TO MODO's NEWSCHOOL NAME
	if 		($symmAxis == "3")	{	$symmAxis = "none";	}
	elsif	($symmAxis == "0")	{	$symmAxis = "x";	}
	elsif	($symmAxis == "1")	{	$symmAxis = "y";	}
	elsif	($symmAxis == "2")	{	$symmAxis = "z";	}
	lxout("turning symm back on ($symmAxis)"); lx("!!select.symmetryState $symmAxis");
}





