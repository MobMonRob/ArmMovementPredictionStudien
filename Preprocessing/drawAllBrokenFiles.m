# draws files in 99_broken dir

function drawAllBrokenFiles(max);
  cd ..\DATA\71_broken
  dirList = glob("*");
  cd ..\..\Preprocessing
  
  maxFileNumber = length(dirList);
  if (max<length(dirList))
    maxFileNumber = max;
  endif
  
  prevFileNumber = 0;
  for i = 1:maxFileNumber
    fileName = dirList{i,1};
    fileNumber = strsplit(fileName,'_'){1,1};
    if(!strcmp(fileNumber,prevFileNumber))
      figure(i);
      drawData(fileNumber,71);
    endif
    prevFileNumber=fileNumber;
  end

end