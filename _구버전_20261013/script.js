document.addEventListener('DOMContentLoaded', function() {
    // Schedule management
    const scheduleForm = document.getElementById('schedule-form');
    const scheduleDateInput = document.getElementById('schedule-date');
    const scheduleTitleInput = document.getElementById('schedule-title');
    const addScheduleBtn = document.getElementById('add-schedule');
    const scheduleList = document.getElementById('schedule-list');

    // Load schedules from localStorage
    let schedules = JSON.parse(localStorage.getItem('schedules') || '[]');

    function renderSchedules() {
        scheduleList.innerHTML = '';
        schedules.forEach((schedule, index) => {
            const li = document.createElement('li');
            li.className = 'schedule-item';
            li.innerHTML = `
                <span>${schedule.date} - ${schedule.title}</span>
                <button data-index="${index}">삭제</button>
            `;
            scheduleList.appendChild(li);
        });
        // Add event listeners to delete buttons
        document.querySelectorAll('#schedule-list button').forEach(btn => {
            btn.addEventListener('click', function() {
                const index = parseInt(this.getAttribute('data-index'));
                schedules.splice(index, 1);
                localStorage.setItem('schedules', JSON.stringify(schedules));
                renderSchedules();
            });
        });
    }

    addScheduleBtn.addEventListener('click', function() {
        const date = scheduleDateInput.value;
        const title = scheduleTitleInput.value.trim();
        if (date && title) {
            schedules.push({ date, title });
            localStorage.setItem('schedules', JSON.stringify(schedules));
            scheduleDateInput.value = '';
            scheduleTitleInput.value = '';
            renderSchedules();
        }
    });

    // Tax calculator
    const taxForm = document.getElementById('tax-form');
    const incomeInput = document.getElementById('income');
    const taxRateInput = document.getElementById('tax-rate');
    const calculateTaxBtn = document.getElementById('calculate-tax');
    const taxResultDiv = document.getElementById('tax-result');

    calculateTaxBtn.addEventListener('click', function() {
        const income = parseFloat(incomeInput.value);
        const taxRate = parseFloat(taxRateInput.value);
        if (!isNaN(income) && !isNaN(taxRate)) {
            const tax = income * (taxRate / 100);
            taxResultDiv.innerHTML = `
                <p>세금: ${tax.toLocaleString()}원</p>
                <p>납부 예상액: ${(income + tax).toLocaleString()}원</p>
            `;
        } else {
            taxResultDiv.innerHTML = '<p>올바른 숫자를 입력해주세요.</p>';
        }
    });

    // Notification functionality
    const requestNotifyBtn = document.getElementById('request-notify');
    const testNotifyBtn = document.getElementById('test-notify');

    function requestNotificationPermission() {
        if ('Notification' in window) {
            Notification.requestPermission().then(permission => {
                if (permission === 'granted') {
                    alert('알림 권한이 허가되었습니다.');
                } else {
                    alert('알림 권한이 거부되었습니다.');
                }
            });
        } else {
            alert('이 브라우저는 알림을 지원하지 않습니다.');
        }
    }

    function showTestNotification() {
        if ('Notification' in window && Notification.permission === 'granted') {
            new Notification('세무 일정 알림 테스트', {
                body: '이것은 테스트 알림입니다.',
                icon: 'https://via.placeholder.com/48'
            });
        } else {
            requestNotificationPermission();
        }
    }

    requestNotifyBtn.addEventListener('click', requestNotificationPermission);
    testNotifyBtn.addEventListener('click', showTestNotification);

    // Initial render
    renderSchedules();
});