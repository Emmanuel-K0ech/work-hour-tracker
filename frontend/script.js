const API = "http://127.0.0.1:8000"

let clockInTime = null

async function loadRoles() {
    const res = await fetch(API + "/roles")
    const roles = await res.json()

    const roleSelect = document.getElementById("roleSelect")
    roles.forEach(role => {
        const option = document.createElement("option")
        option.value = role.id
        option.text = `${role.name} ($${role.hourly_rate}/hr)`
        roleSelect.appendChild(option)
    })
}

async function clockIn() {
    const roleId = document.getElementById("roleSelect").value
    const location = document.getElementById("locationInput").value

    if (!roleId) {
        alert("Please select a role")
        return
    }

    if (!location) {
        alert("Please enter a location")
        return
    }

    try {
        const res = await fetch(API + "/clock-in", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({role_id: parseInt(roleId), location: location})
        })
        const data = await res.json()
        if (res.ok) {
            checkActiveShift()
        } else {
            alert(data.detail || "Error clocking in")
        }
    } catch (e) {
        alert("Error: " + e.message)
    }
}

async function clockOut() {

    try {
        const res = await fetch(API + "/clock-out", {method: "POST"})
        const data = await res.json()
        if (res.ok) {
            clockInTime = null

            if (timerInterval) {
                clearInterval(timerInterval)
                timerInterval = null
            }

            checkActiveShift()
            loadShifts()
            loadTodayHours()
            loadWeeklyChart()
            loadPayBreakdown()
        } else {
            alert(data.detail || "Error clocking out")
        }
    } catch (e) {
        alert("Error: " + e.message)
    }
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
    document.getElementById("totalPay").innerText = "$" + data.total_pay

    const table = document.getElementById("shiftTable")
    table.innerHTML = ""

    data.shifts.forEach(s => {

        const row = `
        <tr>
        <td>${new Date(s.clock_in).toLocaleDateString()}</td>
        <td>${new Date(s.clock_in).toLocaleTimeString()}</td>
        <td>${s.clock_out ? new Date(s.clock_out).toLocaleTimeString() : "-"}</td>
        <td>${s.location || "-"}</td>
        <td>${s.role || "-"}</td>
        <td>${s.hours_worked !== null ? s.hours_worked : "-"}</td>
        <td>${s.pay !== null ? "$" + s.pay : "-"}</td>
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

let weeklyChart = null

async function loadWeeklyChart() {

    const res = await fetch(API + "/weekly-hours")
    const data = await res.json()

    const labels = Object.keys(data)
    const values = Object.values(data)

    const ctx = document.getElementById("weeklyChart")

    // Destroy existing chart if it exists
    if (weeklyChart) {
        weeklyChart.destroy()
    }

    weeklyChart = new Chart(ctx, {
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

async function loadPayBreakdown() {
    const start = document.getElementById("start").value
    const end = document.getElementById("end").value

    let url = API + "/pay-breakdown"

    if (start && end)
        url += `?start=${start}&end=${end}`

    const res = await fetch(url)
    const data = await res.json()

    const container = document.getElementById("payBreakdown")
    container.innerHTML = ""

    if (data.breakdown.length === 0) {
        container.innerHTML = "<p>No shifts recorded</p>"
        return
    }

    let html = `<table style="border-collapse: collapse; width: 100%;">
        <thead>
            <tr style="border: 1px solid #ddd;">
                <th style="border: 1px solid #ddd; padding: 8px;">Role</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Hours</th>
                <th style="border: 1px solid #ddd; padding: 8px;">Pay</th>
            </tr>
        </thead>
        <tbody>`

    data.breakdown.forEach(item => {
        html += `<tr style="border: 1px solid #ddd;">
            <td style="border: 1px solid #ddd; padding: 8px;">${item.role}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">${item.hours}</td>
            <td style="border: 1px solid #ddd; padding: 8px;">$${item.pay}</td>
        </tr>`
    })

    html += `<tr style="border: 1px solid #ddd; font-weight: bold;">
        <td style="border: 1px solid #ddd; padding: 8px;">Total</td>
        <td style="border: 1px solid #ddd; padding: 8px;"></td>
        <td style="border: 1px solid #ddd; padding: 8px;">$${data.total_pay}</td>
    </tr>
    </tbody>
    </table>`

    container.innerHTML = html
}

checkActiveShift()
loadRoles()
loadShifts()
loadTodayHours()
loadWeeklyChart()
loadPayBreakdown()
