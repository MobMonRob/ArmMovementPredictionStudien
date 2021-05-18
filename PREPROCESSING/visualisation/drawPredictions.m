# e.g. drawPredictions()

function drawPredictions(number=10);
    csvPath = ["../../ML/predictions/predicted_real_endpoints.csv"];
    error_file = false;
    try
      A = dlmread(csvPath, ";");
      A = A(2:end,:); #remove first line of zeros
    catch
      error_L = true;
    end_try_catch

    if(error_file)
      disp("Error in both datasets, maybe wrong filename") 
    endif
    figure;
    for i=1:number
        x = [A(i,1); A(i,4)];
        y = [A(i,2); A(i,5)];
        z = [A(i,3); A(i,6)];
        scatter3(x,y,z,100,'filled')
        plot3(x,y,z)
        hold on;
    endfor
    title("Endpoints predictions vs. real");
    xlabel('x');
    ylabel('y');
    zlabel('z');
end
  

