# e.g. drawData(20020403011,0)
# 0 stands for raw

function drawData(csvNumber,phaseNumber);
  phase='';
  switch (phaseNumber)
    case 0
      csvPathLeft = ["./0_raw/" num2str(csvNumber) "_takeover_LGraspPhase.csv"];
      csvPathRight = ["./0_raw/" num2str(csvNumber) "_takeover_RGraspPhase.csv"];
      phase='raw';
    case 1
      phase = 'interpolated';
    case 2
      phase = 'smoothed';
    case 3
      phase = 'truncated';
    case 4 
      phase = 'relocated';
    case 5
      phase = 'filtered';
    otherwise
      phase = 'interpolated';
    endswitch
  if (phaseNumber != 0)
    csvPathLeft = ["./" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_L.csv"];
    csvPathRight = ["./" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_R.csv"];
  endif

  error_L = false;
  error_R = false;
  
  try
    L = dlmread(csvPathLeft, ";");
    L = L(2:end,:); #remove first line of zeros
  catch
    error_L = true;
  end_try_catch
  
  try
    R = dlmread(csvPathRight, ";");
    R = R(2:end,:);
  catch
    error_R = true;
  end_try_catch

  if(error_R && error_L)
    disp("Error in both datasets, maybe wrong filename") 
  endif

  if(error_L)
    plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rechts;",R(:,4),R(:,5),R(:,6), ";Ellenbogen rechts;",R(:,7),R(:,8),R(:,9), ";Schulter rechts;");
  elseif(error_R)
    plot3(L(:,1),L(:,2),L(:,3), ";Handgelenk links;",L(:,4),L(:,5),L(:,6), ";Ellenbogen links;",L(:,7),L(:,8),L(:,9), ";Schulter links;");
  else
    plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rechts;",R(:,4),R(:,5),R(:,6), ";Ellenbogen rechts;",R(:,7),R(:,8),R(:,9), ";Schulter rechts;",L(:,1),L(:,2),L(:,3), ";Handgelenk links;",L(:,4),L(:,5),L(:,6), ";Ellenbogen links;",L(:,7),L(:,8),L(:,9), ";Schulter links;");
  endif
  
  title(strcat(num2str(csvNumber), "-", phase)); #set title
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

