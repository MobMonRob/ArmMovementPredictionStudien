# draws files in 99_broken dir

function drawAllBrokenFiles(max);
  cd ..\DATA\99_broken
  dirList = glob("*_broken_R.csv")
  cd ..\..\Preprocessing
  
  maxFileNumber = length(dirList);
  if (max<length(dirList))
    maxFileNumber = max;
  endif
  
  for i = 1:maxFileNumber
    fileName = dirList{i,1};
    fileNumber = strsplit(fileName,'_'){1,1};
    figure(i);
    drawData(fileNumber,99);
  end

end