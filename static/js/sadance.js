to = 0
pr = 0
ab = 0
pe = 0

tot = document.getElementById('tot')
pre = document.getElementById('pre')
per = document.getElementById('per')
abs = document.getElementById('abs')

tot.innerHTML = 'Total Days: ' + to
pre.innerHTML = 'Present Days: ' + pr
abs.innerHTML = 'Absent Days: ' + ab
per.innerHTML = 'Percentage: ' + pe

function present(){
    to = to+1    
    tot.innerHTML = "Total Days: "+to
    pr = pr+1
    pre.innerHTML = 'Present Days: '+pr
    p1 = pr/to
    pe = p1*100
    per.innerHTML = 'Percentage: ' + pe
}
function absent(){
    to = to+1
    tot.innerHTML = "Total Days: "+to
    ab = ab+1
    abs.innerHTML = 'Absent Days: '+ab
    p1 = pr/to
    pe = p1*100
    per.innerHTML = 'Percentage: ' + pe
}