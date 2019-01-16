
class Controller
{
	constructor(appContainer, fileForm)
	{
		this.setAppContainer(appContainer);
		this.setFileForm(fileForm);
	}
	
	setAppContainer(appContainer)
	{
		this.appContainer = appContainer;
		this.uploadFileContainer = this.appContainer.querySelector('#uploadFileContainer');
		this.processingContainer = this.appContainer.querySelector('#processingContainer');
		this.chartContainer = this.appContainer.querySelector('#chartContainer');
	}
	
	setFileForm(fileForm)
	{
		this.fileForm = fileForm;
		this.fileInput = this.fileForm.querySelector('#dataFile');
		this.fileFormSendButton = this.fileForm.querySelector('#fileSendButton');
		this.csrfToken = this.fileForm.querySelector('input[name=csrfmiddlewaretoken]');
	}
	
	init()
	{
		let controller = this;
		this.fileInput.addEventListener('change', e => controller.handleFileUpload(e), false);
		this.fileFormSendButton.addEventListener('click', e => controller.handleFileSend(e), false);
	}
	
	handleFileUpload(evt)
	{
		let controller = this;
		let infoDiv = document.querySelector('#dataFileInfo');
		
		let file = this.fileInput.files[0];
		
		if(file === null || file === undefined)
        {
			/* KOMUNIKAT O BRAKU PLIKU */
            console.warn('Nie wczytano pliku');
			console.warn(this);
            controller.fileFormSendButton.disabled = true;
            return;
        }

        console.log(file.name);
        console.log(file.size);
        console.log(file.type);
			
		// jezeli wczytano plik JSON
        // w przeciwnym wypadku zablokuj formularz i wypisz komunikat
        if(file.type == "application/json")
        {
            console.log("Wczytano plik JSON!");
			
			infoDiv.innerHTML = "Format pliku OK!";
			controller.fileFormSendButton.classList.remove('btn-danger');
			controller.fileFormSendButton.classList.add('btn-primary');
			
            let fileReader = new FileReader();

            // gdy zakonczy sie metoda fileReader.readAsText, wynik zostanie zapisany
            // do zmiennej, przycisk uaktywniony
            fileReader.addEventListener('load', (event)=>{
                /* SCHOWAJ GIF OCZEKIWANIA */
                /* KOMUNIKAT O POPRAWNIE WPROWADZONYCH DANYCH */
					console.log(event.target.result);
					controller.fileContent = event.target.result;
                    controller.fileFormSendButton.disabled = false;
                }, false);

            // rozpocznij czytanie pliku i ustaw gifa oczekiwania
            /* GIF OCZEKIWANIA */
            fileReader.readAsText(file);

        }
        else
		{
            /* KOMUNIKAT o ZLYM PLIKU */			
			infoDiv.innerHTML = "Format pliku jest niepoprawny!";
            console.warn("Wczytano zły plik!");
			controller.fileFormSendButton.classList.remove('btn-primary');
			controller.fileFormSendButton.classList.add('btn-danger');
            controller.fileFormSendButton.disabled = true;
        }			
	}
	
	handleFileSend(evt)
	{
		evt.preventDefault();
		setTimeout(this.switchPanel(this.processingContainer), 2000);
		
		console.log("Wysylam dane!");
        console.log("Uwaga, bede odbieral dane od serwera");
		
		this.loadData()
		.then(salesData => this.renderChart(salesData))
		.catch(err => console.error(err))
		.finally(() => {
			//this.fileFormSendButton.innerHTML = "Analizuj";
		});
		
	}
	
	switchPanel(panelToShow)
	{
		this.uploadFileContainer.className = "hidden";
		this.processingContainer.className = "hidden";
		this.chartContainer.className = "hidden";
		
		panelToShow.className = "visible";
	}
	
	loadData()
    {
        return new Promise((resolve, reject) => {
			if(this.fileContent === undefined || this.fileContent === null)
				reject("Blad klienta");
			
			//console.log(JSON.stringify(this.fileContent))
            const xhr = new XMLHttpRequest();
			
			//this.fileFormSendButton.innerHTML = "<img src=\"static/Predictor/gifs/loading.gif\"/>"
			console.log(this.csrfToken.value);
            xhr.open('POST', '/predictSales/');
			xhr.setRequestHeader("Content-Type", "application/json");
			xhr.setRequestHeader("X-CSRFToken", this.csrfToken.value);
            xhr.onload = function()
            {
                if(this.status === 200)
                {
                    resolve(JSON.parse(xhr.responseText));
                }
                else
                {
                    reject("Nie udalo sie pobrac danych z bazy");
                }
            };

            xhr.addEventListener('error', ()=> reject(xhr.statusText));
            xhr.send(this.fileContent);
        });
    }

	toggleDataSeries(e) {
		if (typeof (e.dataSeries.visible) === "undefined" || e.dataSeries.visible) {
			e.dataSeries.visible = false;
		} else {
			e.dataSeries.visible = true;
		}
		e.chart.render();
	}
	
	renderChart(salesData)
	{
		let controller = this;
		
		let dataPoints = [];
		let productAvalues = [];
		let productBvalues = [];
		let productCvalues = [];
		let productDvalues = [];
		
		let index = 0;
		
		for(let month in salesData)
		{
			console.log(salesData[month]);
			const {produktA, produktB, produktC, produktD} = salesData[month];
			productAvalues.push({x: index, y: produktA, label: month});
			productBvalues.push({x: index, y: produktB, label: month});
			productCvalues.push({x: index, y: produktC, label: month});
			productDvalues.push({x: index, y: produktD, label: month});
			index++;
			console.log(month);
			//dataPoints.push({x: index++, y: salesData[month], label: month});
		}
		
		console.log(dataPoints);
			
		// wykres przewidywanych danych
		var chart = new CanvasJS.Chart(this.chartContainer.id, {
				exportEnabled: true,
				animationEnabled: true,
				title:{
					text: "Przewidywana sprzedaż"
				},
				subtitles: [{
					text: "Klikaj w legende aby chować lub pokazywać dane"
				}], 
				axisX: {
					title: "Miesiace"
				},
				axisY: {
					title: "Ilosc",
					titleFontColor: "#4F81BC",
					lineColor: "#4F81BC",
					labelFontColor: "#4F81BC",
					tickColor: "#4F81BC"
				},
				toolTip: {
					shared: true
				},
				legend: {
					cursor: "pointer",
					itemclick: controller.toggleDataSeries
				},
				data: [{
					type: "column",
					name: "Produkt A",
					showInLegend: true,      
					yValueFormatString: "#,##0.# Sztuk",
					dataPoints: productAvalues
				},
				{
					type: "column",
					name: "Produkt B",
					showInLegend: true,
					yValueFormatString: "#,##0# Sztuk",
					dataPoints: productBvalues
				},
				{
					type: "column",
					name: "Produkt C",
					showInLegend: true,
					yValueFormatString: "#,##0.# Sztuk",
					dataPoints: productCvalues
				},
				{
					type: "column",
					name: "Produkt D",
					showInLegend: true,
					yValueFormatString: "#,##0.# Sztuk",
					dataPoints: productDvalues
				}]
			});	
		
		
		setTimeout(this.switchPanel(this.chartContainer), 2000);
		
        chart.render();
	}
}