# e.g. drawData(20020403011,0)
# 0 stands for raw

function drawRotated(csvNumber);
  csvPathRaw = ["../DATA/7_filtered/" num2str(csvNumber) "_filtered_R.csv"];
  csvPathRotated = ["../DATA/8_rotated/" num2str(csvNumber) "_rotated_R.csv"];

  error_L = false;
  error_R = false;
  
  try
    A = dlmread(csvPathRaw, ";");
    A = A(2:end,:); #remove first line of zeros
  catch
    error_L = true;
  end_try_catch
  
  try
    R = dlmread(csvPathRotated, ";");
    R = R(2:end,:);
  catch
    error_R = true;
  end_try_catch

  if(error_R && error_L)
    disp("Error in both datasets, maybe wrong filename") 
  endif

  plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rotiert;",A(:,1),A(:,2),A(:,3), ";Handgelenk ursprünglich;");
  title(strcat(num2str(csvNumber), "-rotated")); #set title
  xlabel('x');
  ylabel('y');
  zlabel('z');
end

