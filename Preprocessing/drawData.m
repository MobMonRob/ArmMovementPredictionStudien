# e.g. drawData(20020403011,0)
# 0 stands for raw

function drawData(csvNumber,phaseNumber);
  phase='';
  switch (phaseNumber)
    case 0
      csvPathLeft = ["../DATA/0_raw/" num2str(csvNumber) "_takeover_LGraspPhase.csv"];
      csvPathRight = ["../DATA/0_raw/" num2str(csvNumber) "_takeover_RGraspPhase.csv"];
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
    csvPathLeft = ["../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_L.csv"];
    csvPathRight = ["../DATA/" num2str(phaseNumber) "_" phase "/" num2str(csvNumber) "_" phase "_R.csv"];
  endif

  L = dlmread(csvPathLeft, ";");
  L = L(2:end,:); #remove first line of zeros
  R = dlmread(csvPathRight, ";");
  R = R(2:end,:);
  plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rechts;",R(:,4),R(:,5),R(:,6), ";Ellenbogen rechts;",R(:,7),R(:,8),R(:,9), ";Schulter rechts;",L(:,1),L(:,2),L(:,3), ";Handgelenk links;",L(:,4),L(:,5),L(:,6), ";Ellenbogen links;",L(:,7),L(:,8),L(:,9), ";Schulter links;");
  title(strcat(num2str(csvNumber), "-", phase)); #set title
  xlabel('x');
  ylabel('y');
  zlabel('z');
end
