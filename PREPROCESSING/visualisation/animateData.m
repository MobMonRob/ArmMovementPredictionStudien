# e.g. animateData(20020403011,0,1)
# 0 stands for raw; 0 for left

function animateData(csvNumber,phaseNumber=3, side=1)
  right = false;
  if(side == 1)
    right = true;
  endif
  
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
    otherwise
      phase = 'truncated';
    endswitch
  csvPathLeft = ["../../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_L.csv"];
  csvPathRight = ["../../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_R.csv"];

  error_L = false;
  error_R = false;
  
  if(!right)
    try
      L = dlmread(csvPathLeft, ";");
      L = L(2:end,:); #remove first line of zeros
    catch
      error_L = true;
    end_try_catch
  else
    try
      R = dlmread(csvPathRight, ";");
      R = R(2:end,:);
    catch
      error_R = true;
    end_try_catch
  endif

  if(error_R || error_L)
    disp("Error in dataset, maybe wrong filename") 
  endif

  if(strcmp(phase,'broken') || strcmp(phase, 'broken_prefiltered'))
    try
      broken_file = fileread(csvPathRight);
    catch
      broken_file = fileread(csvPathLeft);
    end_try_catch
    broken_info = strsplit(broken_file,'\n'){1,1};
    title(strcat(num2str(csvNumber), "-",broken_info));
  else
    title(strcat(num2str(csvNumber), "-", phase)); #set title
  endif
  xlabel('x');
  ylabel('y');
  zlabel('z');
  
  if(right)
    h = plot3(R(1,1),R(1,2),R(1,3), ";hand right;");
    axis([min(R(:,1)), max(R(:,1)), min(R(:,2)), max(R(:,2)), min(R(:,3)), max(R(:,3))]);
    for k = 1:length(R);
      set(h, 'XData', R(1:k, 1));
      set(h, 'YData', R(1:k, 2));
      set(h, 'ZData', R(1:k, 3));
      pause (0.02); % delay in seconds
    endfor
  else
    h = plot3(L(1,1),L(1,2),L(1,3), ";hand left;");
    axis([min(L(:,1)), max(L(:,1)), min(L(:,2)), max(L(:,2)), min(L(:,3)), max(L(:,3))]);
    for k = 1:length(L);
      set(h, 'XData', L(1:k, 1));
      set(h, 'YData', L(1:k, 2));
      set(h, 'ZData', L(1:k, 3));
      pause (0.02); % delay in seconds
    endfor
  endif
  

endfunction

