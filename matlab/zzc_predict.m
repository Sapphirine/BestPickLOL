%% Parameters settings
    dataFileName = "filteredTest.csv";
    McoFileName  = "Mco.csv";
    MopFileName  = "Mop.csv";
    % Situation
        aimRows = 1:100;
        aimNumber = 2; % How many recommemds should give
        ban = [0];     % Ban list [Not in use]
    % Columns definition
        winCol = 3;
        ourCols = 14:2:18; % max 14:2:22
        opCols  = 24:2:30; % max 24:2:32
    % Weights
        Wco = 7;
        Wop = 5;

%% Pre-process data
    fprintf("Reading data... ");
    data = readmatrix(dataFileName);
    win = data(:,winCol);
    p0s = data(:,ourCols);
    p1s = data(:,opCols);
    pss = [p0s,p1s];
    Mco = readmatrix(McoFileName);
    Mop = readmatrix(MopFileName);
    fprintf("Done\n")

%% Calculate the recommendations through the input data table
    fprintf("Working...\n");
    if(aimNumber == 1)
        for r = aimRows
            dS_max = 0;
            p_max = 0;
            for n = 1:555
                if(find(pss(r,:)==n)||find(ban(:)==n))
                    continue;
                end
                dSco = 0;
                for k = p0s(r,:)
                    dSco = dSco + Mco(n,k);
                end
                dSop = 0;
                for k = p1s(r,:)
                    dSop = dSop + Mop(n,k);
                end
                dS = dSco*Wco + dSop*Wop;
                if(dS > dS_max)
                    dS_max = dS;
                    p_max = n;
                end
            end
            recommend = p_max;
            fprintf("[%d] R:%d,\n", row, recommend);
            display([[p0s(r,:),0];p1s(r,:)])
        end
    elseif(aimNumber == 2)
        for r = aimRows
            dS_max = 0;
            p_max = 0;
            for n = 1:555
                if(find(pss(r,:)==n))
                    continue;
                end
                for m = n+1:555
                    if(find(pss(r,:)==m))
                        continue;
                    end
                    dSco = 0;
                    for k = p0s(r,:)
                        dSco = dSco + Mco(n,k) + Mco(m,k);
                    end
                    dSop = 0;
                    for k = p1s(r,:)
                        dSop = dSop + Mop(n,k) + Mop(m,k);
                    end
                    dS = dSco*Wco + dSop*Wop;
                    if(dS > dS_max)
                        dS_max = dS;
                        p_max = [n,m];
                    end
                end
            end
            recommend = p_max(:);
            fprintf("[%d] R1:%d, R2:%d\n", r, recommend(1), recommend(2));
            display([p0s(r,:),0,0;p1s(r,:),0])
        end
    else
        error("Only support 1 or 2 heroes, but %d is found.\n", aimNumber);
    end
    fprintf("Mission Complite\n");
    
