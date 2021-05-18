# e.g. drawAllBrokenFiles(20)
# visualize broken files (from filtering)

function drawAllBrokenFiles(max);
  cd ..\..\DATA\99_broken
  dirList = glob("*");
  cd ..\..\Preprocessing\visualisation
  
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
      drawData(fileNumber,99);
    endif
    prevFileNumber=fileNumber;
  end

end