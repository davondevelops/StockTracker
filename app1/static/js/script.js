const date = new Date();

const renderCalendar = () => {
    date.setDate(1);

    const monthDays = document.querySelector(".days");

    const lastDay = new Date(
        date.getFullYear(),
        date.getMonth() + 1,
        0
    ).getDate();

    const prevLastDay = new Date(
        date.getFullYear(),
        date.getMonth(),
        0
    ).getDate();

    const firstDayIndex = date.getDay();

    const lastDayIndex = new Date(
        date.getFullYear(),
        date.getMonth() + 1,
        0
    ).getDay();

    const nextDays = 7 - lastDayIndex - 1;

    const months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ];

    document.querySelector(".date h1").innerHTML = months[date.getMonth()];

    document.querySelector(".date p").innerHTML = new Date().toDateString();

    let days = "";

    for (let x = firstDayIndex; x > 0; x--) {
        days += `<div class="prev-date">${prevLastDay - x + 1}</div>`;
  
    }
    var performanceHist = JSON.parse(document.getElementById('hist').textContent)
    let monthsprofit=0
    let monthsTrades=0
    let wins=0
    let losses=0
    let winnings=0
    console.log(performanceHist);
    for (let i = 1; i <= lastDay; i++) {
        const profitDate= new Date()
        profitDate.setDate(i)
        profitDate.setMonth(date.getMonth())
        profitDate.setYear(date.getFullYear())
        let profitDateformat=(profitDate.getFullYear()+"-"+(profitDate.getMonth()+1)+"-"+profitDate.getDate())
        let profit=0;
        let trades=0;
        for (bx in performanceHist){
            let trade=performanceHist[bx]
            const tradeDate=new Date(trade.fields.dateOfTrade)
            tradeDate.setDate(tradeDate.getDate()+1)

            let tradeDateformat=(tradeDate.getFullYear()+"-"+(tradeDate.getMonth()+1)+"-"+tradeDate.getDate())

            if(tradeDateformat==profitDateformat){
                
                trades++
                if(trade.fields.buy_or_short=="buy"){
                    let tradeProfit=((trade.fields.exit-trade.fields.entry)*trade.fields.position_size)
                    profit+=tradeProfit
                    if (tradeProfit>0){
                        wins++
                        winnings+=tradeProfit
                    }
                    else{losses-=tradeProfit}

                }
                else{
                    let tradeProfit=(trade.fields.entry-trade.fields.exit)*trade.fields.position_size
                    profit+=tradeProfit
                    if (tradeProfit>0){
                        wins++
                        winnings+=tradeProfit
                    }
                    else{losses-=tradeProfit}
                }
                
            }
        }
        
        let daypl=profit.toFixed(2)
        monthsprofit+=parseInt(daypl)
        monthsTrades+=trades
        let color=""
        if(daypl>0){color="green"}
        else if(daypl<0){color="red"}
        else{color="black"}
        // trades=
        if (
            i === new Date().getDate() &&
            date.getMonth() === new Date().getMonth()
        ) {
            days += `<a class="dayrecap" href="/dayrecap/${profitDateformat}"><div class="${color}">
                    <div class="num" >${i}</div>
                    <p>P/L $${daypl}</p>
                    <p>${trades} trades</p>
                </div>
                </a>`;
        } else {
            days += `<a class="dayrecap" href="/dayrecap/${profitDateformat}">
                    <div class="${color}">
                        <div class="num" >${i}</div>
                        <p>P/L: $${daypl}</p>
                        <p>${trades} trades</p>
                    </div> 
                    </a>`;
        }
    }
    let avgWinnings= (winnings/wins).toFixed()
    let avgLoss= (losses/(monthsTrades-wins)).toFixed()
    let winningPer=((wins/monthsTrades)*100).toFixed(2)+"%"
    myDiv = document.getElementById("monthsprofit");
    myDiv.innerHTML=`Month's Profit: $${monthsprofit}`
    myDiv = document.getElementById("monthsTrades");
    myDiv.innerHTML=`# of Trades this Month: ${monthsTrades}`
    myDiv = document.getElementById("winpercentage");
    myDiv.innerHTML=`Winning% this Month: ${winningPer}`
    myDiv = document.getElementById("avgWins");
    myDiv.innerHTML=`Avg Winning: $${avgWinnings}`
    myDiv = document.getElementById("avgLoss");
    myDiv.innerHTML=`Avg Losses: $${avgLoss}`
    
    for (let j = 1; j <= nextDays; j++) {
        days += `<div class="next-date">${j}</div>`;
        monthDays.innerHTML = days;
    }
};

document.querySelector(".prev").addEventListener("click", () => {
    date.setMonth(date.getMonth() - 1);
    renderCalendar();
});

document.querySelector(".next").addEventListener("click", () => {
    date.setMonth(date.getMonth() + 1);
    renderCalendar();
});

renderCalendar();

