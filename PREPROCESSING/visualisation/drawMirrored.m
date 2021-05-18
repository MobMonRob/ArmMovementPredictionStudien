# e.g. drawMirrored(20020403011, 0)
# 0 means original, 1 means right

function drawMirrored(csvNumber, origOrRight);
  csvPathOrig = ["../../DATA/4_prefiltered/" num2str(csvNumber) "_prefiltered_L.csv"];
  csvPathRight = ["../../DATA/4_prefiltered/" num2str(csvNumber) "_prefiltered_R.csv"];
  csvPathMirrored = ["../../DATA/5_mirrored/" num2str(csvNumber) "_mirrored_L.csv"];

  error_O = false;
  error_L = false;
  error_R = false;
  
  try
    O = dlmread(csvPathOrig, ";");
    O = O(2:end,:); #remove first line of zeros
  catch
    error_O = true;
  end_try_catch

  try
    R = dlmread(csvPathRight, ";");
    R = R(2:end,:); #remove first line of zeros
  catch
    error_R = true;
  end_try_catch
  
  try
    L = dlmread(csvPathMirrored, ";");
    L = L(2:end,:);
  catch
    error_L = true;
  end_try_catch

  if origOrRight == 0
    if(error_O && error_L)
      disp("Error in both datasets, maybe wrong filename")
    endif

    if(error_L)
      plot3(O(:,1),O(:,2),O(:,3), ";Handgelenk orig;",O(:,4),O(:,5),O(:,6), ";Ellenbogen orig;",O(:,7),O(:,8),O(:,9), ";Schulter orig;");
    elseif(error_O)
      plot3(L(:,1),L(:,2),L(:,3), ";Handgelenk spiegel;",L(:,4),L(:,5),L(:,6), ";Ellenbogen spiegel;",L(:,7),L(:,8),L(:,9), ";Schulter spiegel;");
    else
      plot3(O(:,1),O(:,2),O(:,3), ";Handgelenk orig;",O(:,4),O(:,5),O(:,6), ";Ellenbogen orig;",O(:,7),O(:,8),O(:,9), ";Schulter orig;",L(:,1),L(:,2),L(:,3), ";Handgelenk spiegel;",L(:,4),L(:,5),L(:,6), ";Ellenbogen spiegel;",L(:,7),L(:,8),L(:,9), ";Schulter spiegel;");
    endif
  else
    if(error_R && error_L)
      disp("Error in both datasets, maybe wrong filename")
    endif

    if(error_L)
      plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rechts;",R(:,4),R(:,5),R(:,6), ";Ellenbogen rechts;",R(:,7),R(:,8),R(:,9), ";Schulter rechts;");
    elseif(error_R)
      plot3(L(:,1),L(:,2),L(:,3), ";Handgelenk spiegel;",L(:,4),L(:,5),L(:,6), ";Ellenbogen spiegel;",L(:,7),L(:,8),L(:,9), ";Schulter spiegel;");
    else
      plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rechts;",R(:,4),R(:,5),R(:,6), ";Ellenbogen rechts;",R(:,7),R(:,8),R(:,9), ";Schulter rechts;",L(:,1),L(:,2),L(:,3), ";Handgelenk spiegel;",L(:,4),L(:,5),L(:,6), ";Ellenbogen spiegel;",L(:,7),L(:,8),L(:,9), ";Schulter spiegel;");
    endif
  endif

  title(num2str(csvNumber)); #set title
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

