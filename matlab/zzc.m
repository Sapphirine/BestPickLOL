% ZZC model
%==============================================
    MODE = "TRAIN";
%::::::::::::::::::::::::::::::::::::::::::::::
    trainFileName = "filteredTrain.csv";
    testFileName = "filteredTest.csv";
    dimention = 100;
%::::::::::::::::::::::::::::::::::::::::::::::
    showMatrix = 0;
    showRate = 1;
    showPosition = 1;
%==============================================

if(MODE == "TRAIN")
    data = readmatrix(trainFileName);
else
    data = readmatrix(testFileName);
end
data = data(:,[3,14:2:32]);
items = size(data,1);
win = data(:,1);
score = zeros(size(win));
p0s = data(:,2:6);
p1s = data(:,7:11);
if(MODE == "TRAIN")
    Mco = zeros(555);
    Mop = zeros(555);
    for r = 1:items
        if win(r) == 1
            score(r) = -1;
        else
            score(r) = 1;
        end
    end
    for r = 1:items
        for n = 1:5
            p0 = p0s(r,n);
            if(p0 == 0)
                continue;
            end
            for m = 1:5
                p0e = p0s(r,m);
                p1 = p1s(r,m);
                if(p0e==0 || p1==0)
                    continue;
                end
                if(p0 ~= p1)
                    Mop(p0,p1) = Mop(p0,p1) + score(r);
                    Mop(p1,p0) = Mop(p1,p0) - score(r);
                end
                if(p0 ~= p0e)
                    Mco(p0,p0e) = Mco(p0,p0e) + score(r);
                end
            end
        end
    end
end
s0co = zeros(items,1);
s1co = zeros(items,1);
sop = zeros(items,1);
for r = 1:items
    for n = 1:5
        p0 = p0s(r,n);
        if(p0 == 0)
            continue;
        end
        for m = 1:5
            p0e = p0s(r,m);
            p1 = p1s(r,m);
            if(p0e==0 || p1==0)
                continue;
            end
            s0co(r) = s0co(r) + Mco(p0,p0e);
            sop(r) = sop(r) + Mop(p0,p1);
        end
    end
    for n = 1:5
        p1 = p1s(r,n);
        if(p1 == 0)
            continue;
        end
        for m = 1:5
            p1e = p1s(r,m);
            if(p1e==0)
                continue;
            end
            s1co(r) = s1co(r) + Mco(p1,p1e);
        end
    end
end
correctRate = zeros(dimention);
for Wco = 1:dimention
    for Wop = 1:dimention
        correct = 0;
        unsure = 0;
        s0 = (s0co-s1co).*Wco + sop.*Wop;
        for r = 1:items
            if(s0(r) > 0 && win(r) == 0)
                correct = correct + 1;
            elseif(s0(r) < 0 && win(r) == 1)
                correct = correct + 1;
            elseif(s0(r) == 0)
                unsure = unsure + 1;
            end
        end
        correctRate(Wco,Wop) = (correct/(items-unsure))*100;
    end
end
if(showMatrix == 1)
    correctRate
end
maxCorrectRate = max(correctRate(:));
if(showRate == 1)
    fprintf("Max Rate: %7.4f",maxCorrectRate);
end
if(showPosition == 1)
    [x,y] = find(correctRate == maxCorrectRate);
    ["Wco","Wop";x,y]
end
