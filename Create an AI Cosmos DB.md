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











