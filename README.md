# Power-Hack

I de siste tiår har utviklingen i internett og digitale teknologier ført til store omveltninger i
flere bransjer. Nå står kraftbransjen midt oppe i denne omveltningen, med de
utfordringene og mulighetene det fører med seg. For Elvia er det svært viktig å følge med og
være med på denne utviklingen.

Smarte strømmålere representerer et viktig ledd i denne digitaliseringen, og finnes nå i alle
norske hjem. Først og fremst er målerne sett på som et verktøy for automatisk avregning og
avlesning av strømforbruk, men mulighetene er mye større enn som så.

I dette hackatonet ønsker Elvia og Computas å bli inspirert av studenter ved å gi dem
anledning til å utvikle et produkt eller en løsning som benytter seg av data fra smarte
strømmålere.

Dere velger selv hvilken målgruppe produktet/løsningen skal være for. Dette kan f.eks.
være forbrukere, nettselskaper eller strømselskaper.

## Datakilder

Dere skal lage et produkt eller en løsning som drar nytte av
data fra de nye AMS-målerne. Dere står fritt til å kombinere data fra AMS-målere med
andre datakilder.

### API for AMS-målere

De nye AMS-målerne registrerer og innrapporterer strømforbruket ditt til nettselskapet, helt ned på timenivå. Via et API kan du få tilgang til (nesten) ekte data fra et utvalg av målerne i Elvia. Her kan du få en liste av tilgjengelige målere og diverse info om dem. Hver av målerne har en ID (meteringpointId), som man kan bruke til å hente ut historiske timesmålinger fra April 2019 fram til August 2021.

Apeiet er beskrevet [her](https://power-hack.azurewebsites.net/swagger/index.html) på en Swagger UI. Her kan man teste ut API'et, se hvilke endepunkter som er tilgjenelig, hva slags inpput parametre som forventes, og hvordan datamodellen ser ut.

De nye AMS-målerne har også en [HAN-port](https://www.elvia.no/smart-forbruk/alt-om-din-strommaler/dette-er-han-porten/), som man kan be om å få åpnet. Data herfra kan for eksempel brukes til å optimalisere smarthjem løsninger eller overvåke ditt eget strømforbruk gir. Når porten er åpnet får du tilgang til forbruksdata og detaljert informasjon om blandt annet strømforbruk i sanntid (real time) og strømforbruket siste timen.

Apiet tilbyr også en [SignalR](https://docs.microsoft.com/en-us/aspnet/core/signalr/introduction?WT.mc_id=dotnet-35129-website&view=aspnetcore-5.0) strøm for hvert av målepunktene som hvert andre sekund sender ut verdier om 
- Forbruk i øyeblikket (Watt)
- Forbruk så langt siden siste timeskift (kwh)
- Tid for målingen
- MålepunktsId
  
Her er eksempel for hvordan man kan koble seg til signalR-streamen C#:
```
using System;
using System.Threading;
using Microsoft.AspNetCore.SignalR.Client;

var hubConnection = new HubConnectionBuilder()
    .WithUrl("https://power-hack.azurewebsites.net/liveMeasurement")
    .Build();
    
await hubConnection.StartAsync();

// Replace <MeteringpointId>
var stream = hubConnection.StreamAsync<object>("Subscribe", <MeteringpointId>);

await foreach (var liveMeasurement in stream)
{
    Console.WriteLine(liveMeasurement);
}
```
Og i javascript:
```
const signalR = require("@microsoft/signalr")

const connection = new signalR.HubConnectionBuilder()
    .withUrl("https://power-hack.azurewebsites.net/liveMeasurement")
    .configureLogging(signalR.LogLevel.Information)
    .build();

async function start() {
    try {
        await connection.start();
        console.log("SignalR Connected.");

        // Replace <MeteringpointId>
        connection.stream("Subscribe", <MeteringpointId>).subscribe({
            next: (item) => console.log(item),
            complete: () => console.log("stream completed"),
            error: (err) => console.log(err)
        })        
    } catch (err) {
        console.log(err);
        setTimeout(start, 5000);
    }
};

start()
```


### Andre datakilder som kan være interessante
 - Strømpriser
 - Nettleiepriser 
 - Værdata
 - Kart


## Nyttige linker
- [Swagger for målere og historisk strømforbruk for disse](https://power-hack.azurewebsites.net/swagger/index.html)
- [Dokumentasjon for SignalR](https://docs.microsoft.com/en-us/aspnet/core/signalr/introduction?WT.mc_id=dotnet-35129-website&view=aspnetcore-5.0)
- [API for Strømpriser]()
- [API fpr Nettleiepriser](https://www.elvia.no/smart-forbruk/api-for-nettleie-priser-kan-gjore-hjemmet-ditt-smartere/)
- [Vær-data i Elvia området](https://elvia.portal.azure-api.net/) Historiske vær-meldinger, observasjoner og lyn-data. (legg til subscribtion til WeatherIngestApi)
- [Mer vær-data](https://frost.met.no/index.html) fra Meteorologisk institutt
