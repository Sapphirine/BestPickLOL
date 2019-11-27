%% Parameters settings
    testFileName = "filteredTest.csv";
    % Columns definition
        winCol = 3;
        ourCols = 14:2:22; % max 14:2:22
        opCols  = 24:2:32; % max 24:2:32
    % Weight
        Wco = 76;
        Wop = 17;

%% Pre-process data
    ourColsNumber = size(ourCols, 2);
    opColsNumber = size(opCols, 2);
    data = readmatrix(testFileName);
    rowNumber = size(data,1);
    win = data(:,winCol);
    p0s = data(:,ourCols);
    p1s = data(:,opCols);

%% Calculate scores
    s0co = zeros(rowNumber,1);
    s1co = zeros(rowNumber,1);
    sop = zeros(rowNumber,1);
    for r = 1:rowNumber
        for n = 1:ourColsNumber
            p0 = p0s(r,n);
            if(p0==0)
                continue;
            end
            for m = 1:ourColsNumber
                p0e = p0s(r,m);
                if(p0e==0)
                    continue;
                end
                s0co(r) = s0co(r) + Mco(p0,p0e);
            end
        end
        for n = 1:opColsNumber
            p1 = p1s(r,n);
            if(p1==0)
                continue;
            end
            for m = 1:opColsNumber
                p1e = p1s(r,m);
                if(p1e==0)
                    continue;
                end
                s1co(r) = s1co(r) + Mco(p1,p1e);
            end
        end
        for n = 1:ourColsNumber
            p0 = p0s(r,n);
            if(p0==0)
                continue;
            end
            for m = 1:opColsNumber
                p1 = p1s(r,m);
                if(p1==0)
                    continue;
                end
                sop(r) = sop(r) + Mop(p0,p1);
            end
        end
    end
    s0 = (s0co-s1co).*Wco + sop.*Wop;
    
%% Test results
    correct = 0;
    unsure = 0;
    for r = 1:rowNumber
        if(s0(r) > 0 && win(r) == 0)
            correct = correct + 1;
        elseif(s0(r) < 0 && win(r) == 1)
            correct = correct + 1;
        elseif(s0(r) == 0)
            unsure = unsure + 1;
        end
    end
    correctRate = (correct/(rowNumber-unsure));
    
%% Show results
    fprintf("Correct Rate: %7.4f\n",correctRate*100);
