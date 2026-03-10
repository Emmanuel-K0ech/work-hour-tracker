const API = "http://127.0.0.1:8000"

let clockInTime = null

async function clockIn() {
    await fetch(API + "/clock-in", {method: "POST"})
    checkActiveShift()
}

async function clockOut() {

    await fetch(API + "/clock-out", {method: "POST"})

    clockInTime = null

    if (timerInterval) {
        clearInterval(timerInterval)
        timerInterval = null
    }

    checkActiveShift()
    loadShifts()
    loadTodayHours()
    loadWeeklyChart()
}

async function checkActiveShift() {

    const res = await fetch(API + "/active-shift")
    const data = await res.json()

    if (data.active) {

        clockInTime = new Date(data.clock_in)

        startTimer()

    } else {

        clockInTime = null
        document.getElementById("timer").innerText = "Not working"

    }
}

let timerInterval = null

function startTimer() {

    if (timerInterval) return

    timerInterval = setInterval(() => {

        if (!clockInTime) return

        let now = new Date()

        let diff = Math.floor((now - clockInTime) / 1000)

        let hours = Math.floor(diff / 3600)
        let minutes = Math.floor((diff % 3600) / 60)
        let seconds = diff % 60

        document.getElementById("timer").innerText =
        `Working: ${hours}h ${minutes}m ${seconds}s`

    }, 1000)
}

async function loadShifts() {

    const start = document.getElementById("start").value
    const end = document.getElementById("end").value

    let url = API + "/shifts"

    if (start && end)
        url += `?start=${start}&end=${end}`

    const res = await fetch(url)
    const data = await res.json()

    document.getElementById("total").innerText = data.total_hours

    const table = document.getElementById("shiftTable")
    table.innerHTML = ""

    data.shifts.forEach(s => {

        const row = `
        <tr>
        <td>${new Date(s.clock_in).toLocaleDateString()}</td>
        <td>${new Date(s.clock_in).toLocaleTimeString()}</td>
        <td>${s.clock_out ? new Date(s.clock_out).toLocaleTimeString() : "-"}</td>
        <td>${s.hours_worked || "-"}</td>
        </tr>
        `

        table.innerHTML += row
    })
}

async function loadTodayHours() {

    const res = await fetch(API + "/today-hours")
    const data = await res.json()

    document.getElementById("todayHours").innerText = data.today_hours
}

async function loadWeeklyChart() {

    const res = await fetch(API + "/weekly-hours")
    const data = await res.json()

    const labels = Object.keys(data)
    const values = Object.values(data)

    const ctx = document.getElementById("weeklyChart")

    new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Hours Worked",
                data: values
            }]
        }
    })
}

checkActiveShift()
loadShifts()
loadTodayHours()
loadWeeklyChart()
