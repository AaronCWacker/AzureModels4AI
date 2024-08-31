# Steps to Create Your First AI DB:

1. Search and find 'Cosmos DB for NoSQL' and Create the Resource.
2. Add a new DB called 'AIDB'
3. Add a new container with these values:
  - Container1
  - /id
  - /name
4. When completed it should look like below.  Delete the other DBs.

<img width="274" alt="image" src="https://github.com/user-attachments/assets/c1afff7a-e589-40b7-96c7-a693ec2be6ec">

# Steps to Add App Logic for AI
1. Use CreateNewPromptRunAgent as name for a new Trigger.  This will be on Create of an Item.
2. Use an AI Prompt to create your first Trigger function.

## Prompts

I'm working in Azure Cosmos DB.  I want to create an intelligent Trigger CreateNewPromptRunAgent that is a pre trigger type with an Operation of Create.  I have Container1 with Items inside.  Complete my Trigger so each time I add a Prompt it creates a record with the prompt text, checks a text pattern and then if it contains any text starting with QT, then it adds each QT Prompt to a new Item.    Use function trigger(){} as a start point and give me logic inside that Trigger to do that.

This trigger function does the following:

Checks if the operation is a "Create" operation.
Retrieves the document (prompt) from the request.
Creates a new record with the prompt text and other metadata.
Checks for text patterns starting with "QT" in the prompt text.
If QT prompts are found, it adds them to the new record and creates separate Items for each QT prompt.
Creates the new record in the container.

The generateGUID() helper function is used to create unique IDs for the new documents.
To use this trigger:

1. Create a new trigger in your Azure Cosmos DB account.
2. Set the trigger type to "Pre-trigger".
3. Set the trigger operation to "Create".
4. Paste this code into the trigger function body.

```Javascript
function trigger() {
    var context = getContext();
    var request = context.getRequest();
    var container = context.getCollection();
    var response = context.getResponse();

    // Check if this is a create operation
    if (request.getOperationType() !== "Create") {
        return;
    }

    // Get the document (prompt) from the request
    var promptDoc = request.getBody();

    // Check if the document has a 'text' property
    if (!promptDoc.text) {
        return;
    }

    // Create a new record with the prompt text
    var newRecord = {
        id: generateGUID(),
        originalPromptId: promptDoc.id,
        promptText: promptDoc.text,
        createdAt: new Date().toISOString()
    };

    // Check for QT patterns
    var qtPrompts = promptDoc.text.match(/QT\s*([^QT]+)/g);

    if (qtPrompts && qtPrompts.length > 0) {
        newRecord.qtPrompts = qtPrompts.map(prompt => prompt.trim());

        // Create a new Item for each QT prompt
        qtPrompts.forEach((qtPrompt, index) => {
            var qtItem = {
                id: generateGUID(),
                originalPromptId: promptDoc.id,
                qtPromptText: qtPrompt.trim(),
                qtPromptIndex: index,
                createdAt: new Date().toISOString()
            };

            // Create the new QT Item
            container.createDocument(container.getSelfLink(), qtItem, 
                function(err, createdDocument) {
                    if (err) throw new Error("Error creating QT Item: " + err.message);
                }
            );
        });
    }

    // Create the new record
    container.createDocument(container.getSelfLink(), newRecord, 
        function(err, createdDocument) {
            if (err) throw new Error("Error creating new record: " + err.message);
        }
    );
}

// Helper function to generate a GUID
function generateGUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

```

This trigger will run every time a new document is created in Container1. It will process the document as described, creating a new record and, if applicable, additional Items for QT prompts.


Now for an input sample we will need a short clip of text for our first document.

This below will do.  QT Means 'Quote Text' and is used by artists to relate themes of art they are sharing.  It is used on Twitter/X when an artist creates a new work of art based on a former theme.

Below is an example of an input that will use the function to split an input into many followup records.  These followup records are created from the input document and can multi-replicate record creation from a thread or batch of queries.

```text
QT Crystal finders: Bioluminescent crystal caverns, quantum-powered explorers, prismatic hues, alien planet
QT robot art: Cybernetic metropolis, sentient androids, rogue AI, neon-infused palette
QT the Lava girl: Volcanic exoplanet, liquid metal rivers, heat-immune heroine, molten metallic palette
QT Underwater Hatch: Submersible alien cityscape, aquanauts, ancient stargate, bioluminescent palette
QT with your 1930s art: Retro-futuristic art deco spaceport, time-traveling agents, sepia-toned futurism
QT with your Alien Beauty on Mars: Terraformed Martian oasis, ethereal alien ambassador, rust-emerald color scheme
QT with your Alien Samurai: Extraterrestrial feudal world, cybernetic ronin, plasma katanas, iridescent metallic
QT with your angel art: Interdimensional celestial nexus, bio-engineered guardians, ethereal luminescence
QT with your bearded man art: Cryogenic revival chamber, dormant captain, generation ship, stark contrasts
QT with your Black and White Art: Monochromatic lunar base, shadow-dwelling aliens, light manipulation, high-contrast grayscale
QT with your colorful art: Psychedelic nebula, living constellations, synesthete navigators, kaleidoscopic explosion
QT with your Cosmic Beauty: Sentient galactic superstructure, energy beings, space-fabric sculpting, cosmic grandeur
QT with your defeat art: Post-apocalyptic Earth, nature reclaimed, human resistance, machine overlords
QT with your gold art: Alchemical space laboratory, transmutation engines, immortality quest, metallic gold-copper
QT with your green art: Biopunk megacity, genetically-modified flora, chlorophyll-enhanced humans, verdant vibrancy
QT with your Knight art: Exoplanet medieval tournament, plasma lances, power-armored knights, technofantasy aesthetic
QT with your Limoncello art: Orbital citrus grove, xenobotanists, intergalactic elixir, zesty yellow mists
QT with your market art: Floating gas giant bazaar, holographic merchants, impossible wares, vibrant alien markets
QT with your Monster Tea Party art: Living spaceship summit, shape-shifting aliens, psychoactive brews, whimsical cosmic horror
QT with your Moon art: Tidal-locked lunar metropolis, gravitational artists, moondustscapes, stark contrasts
QT with your painting art: Virtual reality museum, impossible artworks, AI curators, reality-bending palette
QT with your pilot art: Quantum entanglement cockpit, cyborg pilots, multiverse navigation, sleek futuristic design
QT with your Reverent Silence Art: Interstellar monastery, telepathic monks, forgotten civilizations, muted otherworldly tones
QT with your sailing art: Solar wind spaceship, stellar cartographers, cosmic currents, solar flare palette
QT with your Samurai art: Holographic dojo, space ronin, AI sensei, neo-Tokyo cyberpunk aesthetic
QT with your Tea Time art: Zero-gravity tea ceremony, time-dilating brews, generation ship, delicate cosmic pastels
QT with your Victorian art: Steampunk space elevator, aether-powered automatons, neo-London, brass-fog scheme
QT your assassin: Chameleon-skinned hitman, neon space station, mimicking nanobots, adaptive camouflage
QT your Knight art: Quantum-locked armor, interdimensional peacekeepers, AI weapons, technofantasy fusion
QT your Rocking Horse: Bioengineered low-gravity steeds, neural-linked riders, alien steppes, ethereal starscapes
QT your Selfie: Multidimensional mirror maze, quantum photographers, infinite realities, fractal patterns
QT your Sumo wrestler: Low-gravity martial arts arena, genetically-enhanced athletes, alien physics, dynamic motion
QT with your Alien Art: Hyperdimensional nebula, pulsating alien megalopolis, swirling cosmic plasma
QT with your Pink: Antimatter cascade, cyberpunk metropolis, retina-searing magenta radiation
QT with your New Cartoon Character Art: Reality-bending art gala, anti-gravity vortexes, quantum-entangled extraterrestrials
QT with your Flowers Art: Xenomorphic botanist, sentient bioluminescent ecosystem, chromatic neutron star
QT with your Surreal Art: Fractal crystalline motherships, impossible light spectra, Earth's wonders
QT with your Women in Harmony Art: Hive-mind alien projections, holographic dreamscapes, quantum spacetime fabric
```

# Creating your First Item
Next we want to add the new items into the table.  With your favorite LLM try the following prompt pattern:



```python

# Reformat this for me to put into a new item:


{
    "id": "replace_with_new_document_id",
    "Id": "replace_with_new_partition_key_value"
}



---



QT Crystal finders: Bioluminescent crystal caverns, quantum-powered explorers, prismatic hues, alien planet
QT robot art: Cybernetic metropolis, sentient androids, rogue AI, neon-infused palette
QT the Lava girl: Volcanic exoplanet, liquid metal rivers, heat-immune heroine, molten metallic palette
QT Underwater Hatch: Submersible alien cityscape, aquanauts, ancient stargate, bioluminescent palette
QT with your 1930s art: Retro-futuristic art deco spaceport, time-traveling agents, sepia-toned futurism
QT with your Alien Beauty on Mars: Terraformed Martian oasis, ethereal alien ambassador, rust-emerald color scheme
QT with your Alien Samurai: Extraterrestrial feudal world, cybernetic ronin, plasma katanas, iridescent metallic
QT with your angel art: Interdimensional celestial nexus, bio-engineered guardians, ethereal luminescence
QT with your bearded man art: Cryogenic revival chamber, dormant captain, generation ship, stark contrasts
QT with your Black and White Art: Monochromatic lunar base, shadow-dwelling aliens, light manipulation, high-contrast grayscale
QT with your colorful art: Psychedelic nebula, living constellations, synesthete navigators, kaleidoscopic explosion
QT with your Cosmic Beauty: Sentient galactic superstructure, energy beings, space-fabric sculpting, cosmic grandeur
QT with your defeat art: Post-apocalyptic Earth, nature reclaimed, human resistance, machine overlords
QT with your gold art: Alchemical space laboratory, transmutation engines, immortality quest, metallic gold-copper
QT with your green art: Biopunk megacity, genetically-modified flora, chlorophyll-enhanced humans, verdant vibrancy
QT with your Knight art: Exoplanet medieval tournament, plasma lances, power-armored knights, technofantasy aesthetic
QT with your Limoncello art: Orbital citrus grove, xenobotanists, intergalactic elixir, zesty yellow mists
QT with your market art: Floating gas giant bazaar, holographic merchants, impossible wares, vibrant alien markets
QT with your Monster Tea Party art: Living spaceship summit, shape-shifting aliens, psychoactive brews, whimsical cosmic horror
QT with your Moon art: Tidal-locked lunar metropolis, gravitational artists, moondustscapes, stark contrasts
QT with your painting art: Virtual reality museum, impossible artworks, AI curators, reality-bending palette
QT with your pilot art: Quantum entanglement cockpit, cyborg pilots, multiverse navigation, sleek futuristic design
QT with your Reverent Silence Art: Interstellar monastery, telepathic monks, forgotten civilizations, muted otherworldly tones
QT with your sailing art: Solar wind spaceship, stellar cartographers, cosmic currents, solar flare palette
QT with your Samurai art: Holographic dojo, space ronin, AI sensei, neo-Tokyo cyberpunk aesthetic
QT with your Tea Time art: Zero-gravity tea ceremony, time-dilating brews, generation ship, delicate cosmic pastels
QT with your Victorian art: Steampunk space elevator, aether-powered automatons, neo-London, brass-fog scheme
QT your assassin: Chameleon-skinned hitman, neon space station, mimicking nanobots, adaptive camouflage
QT your Knight art: Quantum-locked armor, interdimensional peacekeepers, AI weapons, technofantasy fusion
QT your Rocking Horse: Bioengineered low-gravity steeds, neural-linked riders, alien steppes, ethereal starscapes
QT your Selfie: Multidimensional mirror maze, quantum photographers, infinite realities, fractal patterns
QT your Sumo wrestler: Low-gravity martial arts arena, genetically-enhanced athletes, alien physics, dynamic motion
QT with your Alien Art: Hyperdimensional nebula, pulsating alien megalopolis, swirling cosmic plasma
QT with your Pink: Antimatter cascade, cyberpunk metropolis, retina-searing magenta radiation
QT with your New Cartoon Character Art: Reality-bending art gala, anti-gravity vortexes, quantum-entangled extraterrestrials
QT with your Flowers Art: Xenomorphic botanist, sentient bioluminescent ecosystem, chromatic neutron star
QT with your Surreal Art: Fractal crystalline motherships, impossible light spectra, Earth's wonders
QT with your Women in Harmony Art: Hive-mind alien projections, holographic dreamscapes, quantum spacetime fabric
```

These items above have structural logic.  Below is output from the LLM which will be used as your first trigger multi-replicator item creation job for AI.

```json
{
  "id": "qt_prompts_collection",
  "originalText": "QT Crystal finders: Bioluminescent crystal caverns, quantum-powered explorers, prismatic hues, alien planet\nQT robot art: Cybernetic metropolis, sentient androids, rogue AI, neon-infused palette\n...",
  "qtPrompts": [
    {
      "title": "Crystal finders",
      "elements": [
        "Bioluminescent crystal caverns",
        "quantum-powered explorers",
        "prismatic hues",
        "alien planet"
      ]
    },
    {
      "title": "robot art",
      "elements": [
        "Cybernetic metropolis",
        "sentient androids",
        "rogue AI",
        "neon-infused palette"
      ]
    },
    {
      "title": "the Lava girl",
      "elements": [
        "Volcanic exoplanet",
        "liquid metal rivers",
        "heat-immune heroine",
        "molten metallic palette"
      ]
    },
    {
      "title": "Underwater Hatch",
      "elements": [
        "Submersible alien cityscape",
        "aquanauts",
        "ancient stargate",
        "bioluminescent palette"
      ]
    },
    {
      "title": "with your 1930s art",
      "elements": [
        "Retro-futuristic art deco spaceport",
        "time-traveling agents",
        "sepia-toned futurism"
      ]
    },
    {
      "title": "with your Alien Beauty on Mars",
      "elements": [
        "Terraformed Martian oasis",
        "ethereal alien ambassador",
        "rust-emerald color scheme"
      ]
    },
    {
      "title": "with your Alien Samurai",
      "elements": [
        "Extraterrestrial feudal world",
        "cybernetic ronin",
        "plasma katanas",
        "iridescent metallic"
      ]
    },
    {
      "title": "with your angel art",
      "elements": [
        "Interdimensional celestial nexus",
        "bio-engineered guardians",
        "ethereal luminescence"
      ]
    },
    {
      "title": "with your bearded man art",
      "elements": [
        "Cryogenic revival chamber",
        "dormant captain",
        "generation ship",
        "stark contrasts"
      ]
    },
    {
      "title": "with your Black and White Art",
      "elements": [
        "Monochromatic lunar base",
        "shadow-dwelling aliens",
        "light manipulation",
        "high-contrast grayscale"
      ]
    },
    {
      "title": "with your colorful art",
      "elements": [
        "Psychedelic nebula",
        "living constellations",
        "synesthete navigators",
        "kaleidoscopic explosion"
      ]
    },
    {
      "title": "with your Cosmic Beauty",
      "elements": [
        "Sentient galactic superstructure",
        "energy beings",
        "space-fabric sculpting",
        "cosmic grandeur"
      ]
    },
    {
      "title": "with your defeat art",
      "elements": [
        "Post-apocalyptic Earth",
        "nature reclaimed",
        "human resistance",
        "machine overlords"
      ]
    },
    {
      "title": "with your gold art",
      "elements": [
        "Alchemical space laboratory",
        "transmutation engines",
        "immortality quest",
        "metallic gold-copper"
      ]
    },
    {
      "title": "with your green art",
      "elements": [
        "Biopunk megacity",
        "genetically-modified flora",
        "chlorophyll-enhanced humans",
        "verdant vibrancy"
      ]
    },
    {
      "title": "with your Knight art",
      "elements": [
        "Exoplanet medieval tournament",
        "plasma lances",
        "power-armored knights",
        "technofantasy aesthetic"
      ]
    },
    {
      "title": "with your Limoncello art",
      "elements": [
        "Orbital citrus grove",
        "xenobotanists",
        "intergalactic elixir",
        "zesty yellow mists"
      ]
    },
    {
      "title": "with your market art",
      "elements": [
        "Floating gas giant bazaar",
        "holographic merchants",
        "impossible wares",
        "vibrant alien markets"
      ]
    },
    {
      "title": "with your Monster Tea Party art",
      "elements": [
        "Living spaceship summit",
        "shape-shifting aliens",
        "psychoactive brews",
        "whimsical cosmic horror"
      ]
    },
    {
      "title": "with your Moon art",
      "elements": [
        "Tidal-locked lunar metropolis",
        "gravitational artists",
        "moondustscapes",
        "stark contrasts"
      ]
    },
    {
      "title": "with your painting art",
      "elements": [
        "Virtual reality museum",
        "impossible artworks",
        "AI curators",
        "reality-bending palette"
      ]
    },
    {
      "title": "with your pilot art",
      "elements": [
        "Quantum entanglement cockpit",
        "cyborg pilots",
        "multiverse navigation",
        "sleek futuristic design"
      ]
    },
    {
      "title": "with your Reverent Silence Art",
      "elements": [
        "Interstellar monastery",
        "telepathic monks",
        "forgotten civilizations",
        "muted otherworldly tones"
      ]
    },
    {
      "title": "with your sailing art",
      "elements": [
        "Solar wind spaceship",
        "stellar cartographers",
        "cosmic currents",
        "solar flare palette"
      ]
    },
    {
      "title": "with your Samurai art",
      "elements": [
        "Holographic dojo",
        "space ronin",
        "AI sensei",
        "neo-Tokyo cyberpunk aesthetic"
      ]
    },
    {
      "title": "with your Tea Time art",
      "elements": [
        "Zero-gravity tea ceremony",
        "time-dilating brews",
        "generation ship",
        "delicate cosmic pastels"
      ]
    },
    {
      "title": "with your Victorian art",
      "elements": [
        "Steampunk space elevator",
        "aether-powered automatons",
        "neo-London",
        "brass-fog scheme"
      ]
    },
    {
      "title": "your assassin",
      "elements": [
        "Chameleon-skinned hitman",
        "neon space station",
        "mimicking nanobots",
        "adaptive camouflage"
      ]
    },
    {
      "title": "your Knight art",
      "elements": [
        "Quantum-locked armor",
        "interdimensional peacekeepers",
        "AI weapons",
        "technofantasy fusion"
      ]
    },
    {
      "title": "your Rocking Horse",
      "elements": [
        "Bioengineered low-gravity steeds",
        "neural-linked riders",
        "alien steppes",
        "ethereal starscapes"
      ]
    },
    {
      "title": "your Selfie",
      "elements": [
        "Multidimensional mirror maze",
        "quantum photographers",
        "infinite realities",
        "fractal patterns"
      ]
    },
    {
      "title": "your Sumo wrestler",
      "elements": [
        "Low-gravity martial arts arena",
        "genetically-enhanced athletes",
        "alien physics",
        "dynamic motion"
      ]
    },
    {
      "title": "with your Alien Art",
      "elements": [
        "Hyperdimensional nebula",
        "pulsating alien megalopolis",
        "swirling cosmic plasma"
      ]
    },
    {
      "title": "with your Pink",
      "elements": [
        "Antimatter cascade",
        "cyberpunk metropolis",
        "retina-searing magenta radiation"
      ]
    },
    {
      "title": "with your New Cartoon Character Art",
      "elements": [
        "Reality-bending art gala",
        "anti-gravity vortexes",
        "quantum-entangled extraterrestrials"
      ]
    },
    {
      "title": "with your Flowers Art",
      "elements": [
        "Xenomorphic botanist",
        "sentient bioluminescent ecosystem",
        "chromatic neutron star"
      ]
    },
    {
      "title": "with your Surreal Art",
      "elements": [
        "Fractal crystalline motherships",
        "impossible light spectra",
        "Earth's wonders"
      ]
    },
    {
      "title": "with your Women in Harmony Art",
      "elements": [
        "Hive-mind alien projections",
        "holographic dreamscapes",
        "quantum spacetime fabric"
      ]
    }
  ],
  "createdAt": "2024-08-31T12:00:00Z"
}
```

Once saved we will have a single item with the normalized language.


![image](https://github.com/user-attachments/assets/5ecd60b4-8dc2-41e3-8765-3dc8f041e0ff)


# Triggers and Stored Procedures to Interact with AI as a Service:

To make this work in your Azure Cosmos DB environment:

Update the trigger:

Go to your Azure Cosmos DB account in the Azure portal.
Navigate to your database and container.
In the "Scale & Settings" section, find the "Triggers" tab.
Create a new trigger or update the existing one with the code from the "Updated Azure Cosmos DB Trigger" artifact.
Set the trigger type to "Pre-trigger" and operation type to "Create".


Create the stored procedure:

In the same container, go to the "Stored Procedures" tab.
Create a new stored procedure named "processPrompt" and paste the code from the "Azure Cosmos DB Stored Procedure" artifact.


Test the setup:

Insert the document you provided into your container.
The trigger should automatically process each QT prompt, calling the stored procedure for each one.
The stored procedure will send a web request for each prompt and create a new document with the response.



Important notes:

Cosmos DB has limitations on stored procedures, including a maximum execution time and no direct internet access. The XMLHttpRequest in the stored procedure is conceptual and won't work as-is. In a real-world scenario, you'd need to use an Azure Function or Logic App to make the HTTP requests.
The trigger and stored procedure assume that the HuggingFace API returns JSON. If it doesn't, you'll need to adjust the response parsing.
Error handling in this example is basic. In a production environment, you'd want more robust error handling and logging.
This setup will create a new document for each QT prompt in the original document. Make sure your container can handle the increased document count and storage.
The URL in the stored procedure is hardcoded. In a real-world scenario, you might want to pass this as a parameter or store it in a configuration document.

To implement this in a production environment, you would need to:

Replace the XMLHttpRequest in the stored procedure with an Azure Function HTTP trigger.
Set up an Azure Function that makes the HTTP request to the HuggingFace API.
Use the Cosmos DB SDK in the Azure Function to create the new document with the API response.
Modify the trigger to call the Azure Function instead of the stored procedure.

This approach would allow you to make external HTTP requests while still leveraging the power of Cosmos DB triggers for automatic processing of new documents.

## Trigger:

```javascript

function trigger() {
    var context = getContext();
    var request = context.getRequest();
    var container = context.getCollection();
    var response = context.getResponse();

    // Check if this is a create operation
    if (request.getOperationType() !== "Create") {
        return;
    }

    // Get the document from the request
    var doc = request.getBody();

    // Check if the document has the expected structure
    if (!doc.qtPrompts || !Array.isArray(doc.qtPrompts)) {
        return;
    }

    // Call the stored procedure for each QT prompt
    doc.qtPrompts.forEach(function(prompt) {
        var sprocLink = container.getAltLink() + "/sprocs/processPrompt";
        var sprocParams = [prompt.title, prompt.elements];
        
        container.executeStoredProcedure(sprocLink, sprocParams, function(err, result) {
            if (err) throw new Error("Error executing stored procedure: " + err.message);
            // You could potentially do something with the result here
        });
    });
}

```


## Stored Procedure

```javascript
function processPrompt(title, elements) {
    var context = getContext();
    var container = context.getCollection();
    var response = context.getResponse();

    // Combine title and elements into a query string
    var query = encodeURIComponent(title + " " + elements.join(" "));
    var url = "https://huggingface.co/spaces/awacke1/ScienceBrain.AI?q=" + query;

    // Send HTTP GET request
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Create a new document with the response
                var newDoc = {
                    id: generateGUID(),
                    originalPrompt: {
                        title: title,
                        elements: elements
                    },
                    aiResponse: JSON.parse(xhr.responseText),
                    createdAt: new Date().toISOString()
                };

                // Insert the new document
                container.createDocument(container.getSelfLink(), newDoc, function(err, createdDoc) {
                    if (err) throw new Error("Error creating document: " + err.message);
                    response.setBody(createdDoc);
                });
            } else {
                throw new Error("HTTP request failed with status: " + xhr.status);
            }
        }
    };
    xhr.send();

    // Helper function to generate a GUID
    function generateGUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
}
```

Once completed it should look like this.  The trigger will accept new multiple part records as a document.  It will call the stored procedure which will then call the web application which follows the search engine query parameter ?q= pattern used by other search engines as a simple GET pattern.


![image](https://github.com/user-attachments/assets/8d3a1b2e-fa13-4add-bfda-9f17bf03050b)


Now that we have the basic design layed out when can refactor to make it work.

Lets create a new Azure function..
1. Go to resource group:
![image](https://github.com/user-attachments/assets/2a576127-8668-4b84-b184-f83ec9522809)
2. Search Azure Function (app):
![image](https://github.com/user-attachments/assets/6d8e8ce0-9114-4ca5-8bea-745e02700c47)
3. Add it:
![image](https://github.com/user-attachments/assets/0c6ecba5-0b92-4f56-aee5-2beb694ea0b1)

Make sure the region is the same as your Cosmos DB.  Below it is Central:
![image](https://github.com/user-attachments/assets/298ebef9-2f1b-435a-9537-0aae33d23d1c)

Set to Python and give it a name.  Below I use ai01-app.


![image](https://github.com/user-attachments/assets/7e84b25d-38ab-4d41-abad-276ae8c3d6b1)

# Create Azure Function and Stored Procedure to call ScienceBrain and save results.  

This is loosely coupling the Azure Function, the Huggingface Python Streamlit App with Query Parameter Inferencing, and the Azure Cosmos DB to run it all. These three components together are infinitely scalable and form a data storage and control process with preprocessing in our Azure Cosmos DB which allows us to do cool things!

Let's create an Azure Function to handle the HTTP request and a new stored procedure to call this function.

First, let's create an Azure Function:
1. Azure Function: ProcessPromptClick to open code
2. Now, let's create a new stored procedure that will call this Azure Function:
3. Updated Azure Cosmos DB Stored Procedure:
4. processPrompt

To implement this solution:
  Deploy the Azure Function:

Create a new Function App in Azure.

Create a new HTTP-triggered function and paste the code from the "Azure Function: ProcessPrompt" artifact.

Make sure to install the axios and @azure/cosmos packages in your Function App.

Set up the following application settings in your Function App:

**CosmosDBConnectionString**: Your Cosmos DB connection string
**DatabaseName**: Your database name
**ContainerName**: Your container name




Update the stored procedure:

In your Cosmos DB container, go to the "Stored Procedures" tab.
Create a new stored procedure named "processPrompt" and paste the code from the "Updated Azure Cosmos DB Stored Procedure" artifact.
Replace "https://your-function-app.azurewebsites.net/api/ProcessPrompt" with the actual URL of your deployed Azure Function.  Mine will be https://ai01-app.azurewebsites.net/api/ProcessPrompt


Update the trigger (if necessary):

If you're still using a trigger, update it to call this new stored procedure instead of the old one.



This setup addresses the previous issues:

The HTTP request is now made by the Azure Function, which has full internet access.
The Azure Function can handle any response format from the HuggingFace API. If it's not JSON, you can modify the function to parse it appropriately.
The Azure Function creates the new document in Cosmos DB, so we don't need to worry about doing that in the stored procedure.
Error handling is improved, with errors logged in the Azure Function.

Remember to secure your Azure Function appropriately, possibly using Azure AD authentication or function keys, to prevent unauthorized access.
This solution provides a more robust and scalable approach to processing your prompts and interacting with external APIs while leveraging the power of Cosmos DB triggers and stored procedures.

# Azure Function
```javascript
const axios = require('axios');
const { CosmosClient } = require('@azure/cosmos');

module.exports = async function (context, req) {
    context.log('JavaScript HTTP trigger function processed a request.');

    const title = req.body.title;
    const elements = req.body.elements;

    if (!title || !elements) {
        context.res = {
            status: 400,
            body: "Please pass a title and elements in the request body"
        };
        return;
    }

    try {
        // Combine title and elements into a query string
        const query = encodeURIComponent(`${title} ${elements.join(" ")}`);
        const url = `https://huggingface.co/spaces/awacke1/ScienceBrain.AI?q=${query}`;

        // Make the HTTP request
        const response = await axios.get(url);

        // Create a new document with the response
        const newDoc = {
            id: generateGUID(),
            originalPrompt: {
                title: title,
                elements: elements
            },
            aiResponse: response.data,
            createdAt: new Date().toISOString()
        };

        // Insert the new document into Cosmos DB
        const cosmosClient = new CosmosClient(process.env.CosmosDBConnectionString);
        const container = cosmosClient.database(process.env.DatabaseName).container(process.env.ContainerName);
        const { resource: createdItem } = await container.items.create(newDoc);

        context.res = {
            status: 200,
            body: createdItem
        };
    } catch (error) {
        context.log(`Error: ${error.message}`);
        context.res = {
            status: 500,
            body: `Error processing request: ${error.message}`
        };
    }
};

function generateGUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = Math.random() * 16 | 0, v = c == 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
```

# Updated stored procedure
```javascript
function processPrompt(title, elements) {
    var context = getContext();
    var container = context.getCollection();
    var response = context.getResponse();

    var azureFunctionUrl = "https://your-function-app.azurewebsites.net/api/ProcessPrompt";

    var requestBody = {
        title: title,
        elements: elements
    };

    var isComplete = false;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", azureFunctionUrl, true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // The Azure Function has already created the document in Cosmos DB
                // We just need to return the response
                response.setBody(JSON.parse(xhr.responseText));
            } else {
                throw new Error("Azure Function request failed with status: " + xhr.status);
            }
            isComplete = true;
        }
    };
    xhr.send(JSON.stringify(requestBody));

    while (!isComplete) {
        context.getResponse().setBody("Processing...");
    }
}

```

Note - Set Basic auth and enable it to ccontinuous deploy on Change to a git repo.  Shown is the current git repo:


![image](https://github.com/user-attachments/assets/ebc8b853-1b5d-421f-ba96-f2f055a6557a)



![image](https://github.com/user-attachments/assets/91835c2b-e6da-4aad-8d08-b78157520b8d)


![image](https://github.com/user-attachments/assets/ac4eebd8-6e2e-496d-b635-fe343f41a77f)

# Continuous deployment

```javascript

# Docs for the Azure Web Apps Deploy action: https://github.com/azure/functions-action
# More GitHub Actions for Azure: https://github.com/Azure/actions
# More info on Python, GitHub Actions, and Azure Functions: https://aka.ms/python-webapps-actions

name: Build and deploy Python project to Azure Function App - ai01-app

on:
  push:
    branches:
      - main
  workflow_dispatch:

env:
  AZURE_FUNCTIONAPP_PACKAGE_PATH: '.' # set this to the path to your web app project, defaults to the repository root
  PYTHON_VERSION: '3.11' # set this to the python version to use (supports 3.6, 3.7, 3.8)

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Setup Python version
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}

      - name: Create and start virtual environment
        run: |
          python -m venv venv
          source venv/bin/activate

      - name: Install dependencies
        run: pip install -r requirements.txt

      # Optional: Add step to run tests here

      - name: Zip artifact for deployment
        run: zip release.zip ./* -r

      - name: Upload artifact for deployment job
        uses: actions/upload-artifact@v4
        with:
          name: python-app
          path: |
            release.zip
            !venv/

  deploy:
    runs-on: ubuntu-latest
    needs: build
    environment:
      name: 'production'
      url: ${{ steps.deploy-to-function.outputs.webapp-url }}
    
    steps:
      - name: Download artifact from build job
        uses: actions/download-artifact@v4
        with:
          name: python-app

      - name: Unzip artifact for deployment
        run: unzip release.zip     
        
      - name: 'Deploy to Azure Functions'
        uses: Azure/functions-action@v1
        id: deploy-to-function
        with:
          app-name: 'ai01-app'
          slot-name: 'production'
          package: ${{ env.AZURE_FUNCTIONAPP_PACKAGE_PATH }}
          scm-do-build-during-deployment: true
          enable-oryx-build: true
          publish-profile: ${{ secrets.AzureAppService_PublishProfile_1234 }}

```


# Retry using external connection from Streamlit Huggingface app.

![image](https://github.com/user-attachments/assets/e6051b85-16f8-46d9-a47e-da0a9d65fba0)


```python

import streamlit as st
from azure.cosmos import CosmosClient
import os

# Cosmos DB configuration
ENDPOINT = "https://acae-afd.documents.azure.com:443/"
SUBSCRIPTION_ID = "003fba60-5b3f-48f4-ab36-3ed11bc40816"

# You'll need to set these environment variables or use Azure Key Vault
DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER_NAME")

def insert_record(record):
    try:
        response = container.create_item(body=record)
        return True, response
    except Exception as e:
        return False, str(e)

# Streamlit app
st.title("🌟 Cosmos DB Record Insertion")

# Login section
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.subheader("🔐 Login")
    input_key = st.text_input("Enter your Cosmos DB Primary Key", type="password")
    if st.button("🚀 Login"):
        if input_key:
            st.session_state.primary_key = input_key
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Please enter a valid key")
else:
    # Initialize Cosmos DB client
    client = CosmosClient(ENDPOINT, credential=st.session_state.primary_key)
    database = client.get_database_client(DATABASE_NAME)
    container = database.get_container_client(CONTAINER_NAME)

    # Input fields
    st.subheader("📝 Enter Record Details")
    id = st.text_input("ID")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0, max_value=150)
    city = st.text_input("City")

    # Submit button
    if st.button("💾 Insert Record"):
        record = {
            "id": id,
            "name": name,
            "age": age,
            "city": city
        }
        
        success, response = insert_record(record)
        if success:
            st.success("✅ Record inserted successfully!")
            st.json(response)
        else:
            st.error(f"❌ Failed to insert record: {response}")

    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # Display connection info
    st.sidebar.subheader("🔗 Connection Information")
    st.sidebar.text(f"Endpoint: {ENDPOINT}")
    st.sidebar.text(f"Subscription ID: {SUBSCRIPTION_ID}")
    st.sidebar.text(f"Database: {DATABASE_NAME}")
    st.sidebar.text(f"Container: {CONTAINER_NAME}")

```

# Next create it as streamlit app on HF:

# You'll need to set these environment variables by adding to Space secrets.
1. DATABASE_NAME = os.environ.get("COSMOS_DATABASE_NAME")
2. CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER_NAME")
3. COSMOS_DATABASE_NAME = AIDB
4. COSMOS_CONTAINER_NAME = Container1

![image](https://github.com/user-attachments/assets/4e646562-10b3-49d0-b93c-74f6928db797)


