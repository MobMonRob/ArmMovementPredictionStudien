# e.g. drawData(20020403011,0)
# 0 stands for raw

function drawData(csvNumber,phaseNumber);
  phase='';
  switch (phaseNumber)
    case 0
      phase='raw';
    case 1
      phase = 'interpolated';
    case 2
      phase = 'smoothed';
    case 3
      phase = 'truncated';
    case 4
      phase = 'prefiltered';
    case 5 
      phase = 'mirrored';
    case 6
      phase = 'relocated'
    case 7
      phase = 'filtered';
    case 98
      phase = 'broken_prefiltered';
    case 99
      phase = 'broken';
    case 71
      phase = 'broken';
    otherwise
      phase = 'truncated';
    endswitch
  csvPathLeft = ["../../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_L.csv"];
  csvPathRight = ["../../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_R.csv"];

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
    plot3(R(:,1),R(:,2),R(:,3), ";hand right;",R(:,4),R(:,5),R(:,6), ";elbow right;",R(:,7),R(:,8),R(:,9), ";shoulder right;");
  elseif(error_R)
    plot3(L(:,1),L(:,2),L(:,3), ";hand left;",L(:,4),L(:,5),L(:,6), ";elbow left;",L(:,7),L(:,8),L(:,9), ";shoulder left;");
  else
    plot3(R(:,1),R(:,2),R(:,3), ";hand right;",R(:,4),R(:,5),R(:,6), ";elbow right;",R(:,7),R(:,8),R(:,9), ";shoulder right;",L(:,1),L(:,2),L(:,3), ";hand left;",L(:,4),L(:,5),L(:,6), ";elbow left;",L(:,7),L(:,8),L(:,9), ";shoulder left;");
  endif
  
  if(strcmp(phase,'broken') || strcmp(phase, 'broken_prefiltered'))
    try
      broken_info_right = strsplit(fileread(csvPathRight),'\n'){1,1};
    catch
      broken_info_right = "";
    end_try_catch
    try
      broken_info_left = strsplit(fileread(csvPathLeft),'\n'){1,1};
    catch
      broken_info_left = "";
    end_try_catch
    
    title(strcat(num2str(csvNumber), "\nR: ",broken_info_right,"\nL: ",broken_info_left));
  else
    title(strcat(num2str(csvNumber), "-", phase)); #set title
  endif
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

