# e.g. drawAllFiles(3,'R','all')
# side can be 'R', 'L' or 'both'
# bodyPart can be 'hand', 'elbow', 'shoulder' or 'all'

function drawAllFiles(phaseNumber=4, side='both',bodyPart='hand');
    phase='';
    switch (phaseNumber)
        case 0
            phase='raw';
        case 1
            phase = 'interpolated';
        case 2
            phase = 'smoothed';
        case 3
            phase = 'truncated';
        case 4
            phase = 'prefiltered';
        case 5 
            phase = 'mirrored';
        case 6
            phase = 'relocated'
        case 7
            phase = 'filtered';
        case 8
            phase = 'rotated';
        case 98
            phase = 'broken_prefiltered';
        case 99
            phase = 'broken';
        endswitch
    directory = ["../../DATA/" num2str(phaseNumber) "_" phase ];
    cd(directory)

    if(!strcmp(side,'both'))
        dirList = glob(["*" side ".csv"]);
    else
        dirList = glob("*");
    endif
    cd('../../PREPROCESSING/visualisation')
    maxFileNumber = length(dirList);
    figure;
    for i = 1:maxFileNumber
        fileName = dirList{i,1};
        fileNumber = strsplit(fileName,'_'){1,1}
        sideCSV = strsplit(fileName,'_'){1,3};
        csvPath = [ directory "/" num2str(fileNumber) "_" phase "_" sideCSV];
        A = dlmread(csvPath, ";");
        A = A(2:end,:); #remove first line of zeros

        if(strcmp(bodyPart,'hand'))
            plot3(A(:,1),A(:,2),A(:,3));
        elseif(strcmp(bodyPart, 'elbow'))
            plot3(A(:,4),A(:,5),A(:,6))
        elseif(strcmp(bodyPart, 'shoulder'))
            plot3(A(:,7),A(:,8),A(:,9))
        else
            plot3(A(:,1),A(:,2),A(:,3), A(:,4),A(:,5),A(:,6), A(:,7),A(:,8),A(:,9));
        endif
        if(phaseNumber==8)
            scatter3(A(70,1),A(70,2),A(70,3),100,'filled')
        endif
        hold on;
    endfor
    xlabel('x');
    ylabel('y');
    zlabel('z');
    title(["All " phase " files: body part: " bodyPart ", side: " side])
end
  

