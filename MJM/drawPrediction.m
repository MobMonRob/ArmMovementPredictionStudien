# e.g. drawData(20020403011, 0)
# 0 is right, 1 is left

function drawPrediction(csvNumber, right_or_left);
  if right_or_left == 0
    csvPathOrig = ["../DATA/7_filtered/" num2str(csvNumber) "_filtered_R.csv"];
    csvPathPred = ["./Prediction/" num2str(csvNumber) "_predicted_R.csv"];
  else
    csvPathOrig = ["../DATA/7_filtered/" num2str(csvNumber) "_filtered_L.csv"];
    csvPathPred = ["./Prediction/" num2str(csvNumber) "_predicted_L.csv"];
  endif

  error_O = false;
  error_P = false;

  try
    O = dlmread(csvPathOrig, ";");
    O = O(2:end,:); #remove first line of zeros
  catch
    error_O = true;
  end_try_catch

  try
    P = dlmread(csvPathPred, ";");
    P = P(2:end,:);
  catch
    error_P = true;
  end_try_catch

  if(error_O && error_P)
    disp("Error in both datasets, maybe wrong filename")
  endif

  if(error_P)
    plot3(O(:,1),O(:,2),O(:,3), ";Handgelenk Original;");
  elseif(error_O)
    plot3(P(:,1),P(:,2),P(:,3), ";Handgelenk Vorhersage;");
  else
    plot3(O(:,1),O(:,2),O(:,3), ";Handgelenk Original;",P(:,1),P(:,2),P(:,3), ";Handgelenk Vorhersage;");
  endif

  title(num2str(csvNumber)); #set title
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

