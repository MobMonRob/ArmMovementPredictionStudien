# e.g. drawPoints('endpoints_42')

function drawPoints(filenumber)
    csvPath = ["../DATA/97_endpoints/" filenumber ".csv"];
    error = false;
    try
      D = dlmread(csvPath, ";");
      D = D(2:end,:); #remove first line of zeros
    catch
      error = true;
    end_try_catch

    if(error)
        disp("Error in dataset, maybe wrong filename") 
    endif

    scatter3 (D(:,1), D(:,2), D(:,3))
    title(filenumber));

  
  

endfunction

