# e.g. drawPoints('endpoints_42')

function drawPoints(side)
    csvPath1 = ["../DATA/97_endpoints/endpoints_0305_" side ".csv"];
    csvPath2 = ["../DATA/97_endpoints/endpoints_0403_" side ".csv"];
    csvPath3 = ["../DATA/97_endpoints/endpoints_0423_" side ".csv"];
    error = false;
    try
      D1 = dlmread(csvPath1, ";");
      D2 = dlmread(csvPath2, ";");
      D3 = dlmread(csvPath3, ";");
    catch
      error = true;
    end_try_catch

    if(error)
        disp("Error in dataset, maybe wrong filename") 
    endif

    scatter3 (D1(:,1), D1(:,2), D1(:,3));
    hold on;
    scatter3 (D2(:,1), D2(:,2), D2(:,3));
    scatter3 (D3(:,1), D3(:,2), D3(:,3));

  
  

endfunction

