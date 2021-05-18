# e.g. drawRotated(20020403011)

function drawRotated(csvNumber);
  if(csvNumber==0)
    cd ..\..\DATA\8_rotated
    dirList = glob("*");
    cd ..\..\visualisation\Preprocessing
    maxFileNumber = length(dirList);
    figure;
    for i = 1:maxFileNumber
        fileName = dirList{i,1};
        fileNumber = strsplit(fileName,'_'){1,1}
        side = strsplit(fileName,'_'){1,3};
        csvPathRotated = ["../DATA/8_rotated/" num2str(fileNumber) "_rotated_" side];
        A = dlmread(csvPathRotated, ";");
        A = A(2:end,:); #remove first line of zeros
        plot3(A(:,1),A(:,2),A(:,3), 'linestyle','--')
        scatter3(A(80,1),A(80,2),A(80,3),100,'filled')
        hold on;
    endfor
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title('Alle rotierten Dateien')
  else
    csvPathRaw = ["../../DATA/7_filtered/" num2str(csvNumber) "_filtered_R.csv"];
    csvPathRotated = ["../../DATA/8_rotated/" num2str(csvNumber) "_rotated_R.csv"];

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
    figure;
    plot3(R(:,1),R(:,2),R(:,3), ";Handgelenk rotiert;",A(:,1),A(:,2),A(:,3), ";Handgelenk urspruenglich;", 'linestyle','--');
    hold on;
    scatter3(A(80,1),A(80,2),A(80,3),50)
    scatter3(R(80,1),R(80,2),R(80,3),100,'filled')
    title(strcat(num2str(csvNumber), "-rotated")); #set title
    xlabel('x');
    ylabel('y');
    zlabel('z');
  endif
end
  

