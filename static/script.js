

document.addEventListener('DOMContentLoaded', () => {
    const predictionDataElement = document.getElementById('prediction-data');
    const refreshButton = document.getElementById('refresh-button');
    const regionSelect = document.getElementById('region-select');
    const metaInfo = document.getElementById('meta-info');


    const showLoader = () => {
        predictionDataElement.innerHTML = `
            <div class="loader-container">
                <div class="loader"></div>
                <p>Завантаження прогнозу...</p>
            </div>
        `;
    };


    const showError = (message) => {
        predictionDataElement.innerHTML = `
            <div class="error">
                <p>⚠️ ${message}</p>
            </div>
        `;
    };


    const displayMeta = (data) => {
        if (!metaInfo) return;
        const trainTime = data.last_model_train_time || '—';
        const predTime = data.last_prediction_time || '—';
        const modelName = data.model_name || '—';
        metaInfo.innerHTML = `
            <span>🤖 Модель: <strong>${modelName}</strong></span>
            <span>🎓 Тренування: <strong>${trainTime}</strong></span>
            <span>🔄 Прогноз: <strong>${predTime}</strong></span>
            <span>🌍 Регіонів: <strong>${data.total_regions || '—'}</strong></span>
        `;
    };


    const displayForecasts = (regionsData) => {
        predictionDataElement.innerHTML = '';

        if (!regionsData || Object.keys(regionsData).length === 0) {
            showError('Немає даних прогнозу');
            return;
        }

        Object.entries(regionsData).forEach(([regionName, hourlyData]) => {

            const regionCard = document.createElement('div');
            regionCard.classList.add('region-card');


            const nameEl = document.createElement('h2');
            nameEl.classList.add('region-name');
            nameEl.textContent = regionName;


            const forecastDiv = document.createElement('div');
            forecastDiv.classList.add('hourly-forecast');


            const currentHour = new Date().getHours();

            Object.entries(hourlyData).forEach(([timeKey, isAlarm]) => {
                const hour = parseInt(timeKey.split(':')[0], 10);

                const hourCol = document.createElement('div');
                hourCol.classList.add('hour-column');


                if (hour === currentHour) {
                    hourCol.classList.add('current-hour');
                }


                const label = document.createElement('div');
                label.classList.add('hour-label');
                label.textContent = timeKey;


                const block = document.createElement('div');
                block.classList.add('prediction-block');
                block.classList.add(isAlarm ? 'alarm-true' : 'alarm-false');
                block.title = isAlarm
                    ? `${timeKey}: ⚠️ Тривога очікується`
                    : `${timeKey}: ✅ Тривоги немає`;

                hourCol.appendChild(label);
                hourCol.appendChild(block);
                forecastDiv.appendChild(hourCol);
            });

            regionCard.appendChild(nameEl);
            regionCard.appendChild(forecastDiv);
            predictionDataElement.appendChild(regionCard);
        });
    };


    const fetchForecasts = async () => {
        showLoader();
        try {
            const selectedRegion = regionSelect ? regionSelect.value : 'all';

            const response = await fetch('/api/forecast', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ region: selectedRegion })
            });

            if (!response.ok) throw new Error(`HTTP ${response.status}`);

            const data = await response.json();
            displayMeta(data);
            displayForecasts(data.regions_forecast);
        } catch (error) {
            console.error('Помилка завантаження:', error);
            showError('Не вдалося завантажити прогноз. Спробуйте пізніше.');
        }
    };


    const refreshPredictions = async () => {
        showLoader();
        refreshButton.disabled = true;
        refreshButton.textContent = '⏳ Оновлення...';

        try {
            const response = await fetch('/api/refresh', {
                method: 'POST'
            });

            if (!response.ok) {
                const err = await response.json();
                throw new Error(err.error || `HTTP ${response.status}`);
            }

            const data = await response.json();
            displayMeta(data);
            displayForecasts(data.regions_forecast);
        } catch (error) {
            console.error('Помилка оновлення:', error);
            showError(`Помилка оновлення: ${error.message}`);
        } finally {
            refreshButton.disabled = false;
            refreshButton.textContent = '🔄 Refresh';
        }
    };


    refreshButton.addEventListener('click', refreshPredictions);


    if (regionSelect) {
        regionSelect.addEventListener('change', fetchForecasts);
    }


    fetchForecasts();


    setInterval(fetchForecasts, 60000);
});