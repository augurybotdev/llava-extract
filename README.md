# llava-extract
llava 1.5 comp vision with llm intelligence fine tuned on custom dataset of US drivers licenses for text extraction super powers

## Current State - Next Steps:

- About This Project: Why am I trying to extract the text from Drivers Licenses using a cutting edge advanced multi-modal ai?

- I was approached by potential client looking for developers to work on a project. I was encouraged to submit a proposal. The potential client wanted a specialty OCR that could reliably extract the text from an image of an ID and accurately collect it into a form or database. Seeing an opportunity here, whilst not having much direct experience with OCR's I went for it and gave it my best shot. 

- Instead of simply applying, I took a few hours and developed an online demo show-casing 2 different approaches. Both of these demos implemented the basic tech needed, depending on 2 different fundamental considerations. One demo considers a locally hosted concept that would be completely customizable and fine-tunable and then another one utilizing a service (Google CV) for an out of box solution but free for demo purposes. I did not yet know what the potential client's needs were, so I wanted to show that I could flexibly adapt to their unique situation.

<sub> while not the greatest examples, they are working examples and perform the essential functions of the desired outcomes. you can check it out [https://github.com/augurybotdev/OCR-based-ID-Scraper](here)</sub> 

After submitting my proposal, I received no further correspondence. I had little expectations regardless and normally would never go this far when responding to a request for a proposal in this way. I considered it an experiment.

However, I still pondered what other solution I could have provided? How could I have improved my proposal? I decided to dig a little deeper and question the tech stack I was using in my demos. A couple years ago I would have thought OCR ai tech to be quite amazing. Now, what is amazing to me is our ability to rapidly adapt to not only technological progress, but the *rate* at which it changes. Anyways, the multi-model ai cnn's are just as capable if not more so than almost all deployed uses of OCR tech, especially on general extraction tasks. If I am building something on my own, I am going to use all of the power tools available to me to accomplish the goal, within the constraints in order to provide the best outcome at a value I can afford. With this in mind, a multi-model llm with computer vision is quite the amazing general use case tool...

The real fun happens once the model provides it's text response to your instructions. Compared to the response from any OCR, and it's obvious why this is the better way. My 21st century spoiled brain is already thinking,  "Why can't I just tell the ai to give me the text that i want and only the text that i want in the way that i want it?" I decided I should investigate this. 

It turns out that State Issued Drivers Licenses are actually a really difficult use case for text extraction. If you take a second to thing about it, they were designed this way on purpose. To conquer this area would be to validate the concept. Text extracted from images of state issued drivers licenses, taken by people in an arbitrary manner, accurately and consistently, is a challenge for any OCR. 

As it is currently though, with just a few adjustments the Llava 1.5 model ALMOST gets all of the data fields and values correctly extracted. With some prompt engineering and experimentation, it ets it even closer. To push this over the edge however, I should fine tune on a custom dataset.
I am shooting for 100 % accuracy (aim high right?)

The idea is to make this better than any current ocr or human for that matter, when it comes to extracting text from an image. As of now, it is widely contingent on things such as the state of issuance, year that it was issued, quality of photo, etc… 

1. extract the text from the image.
    - prompt engineer to guide the model to return the text from the image in a format that is useful (json)
    - run the program and pass the image + prompt to the model
2. compile this information into SQL database. 
    - get results and compile into database
    - As the model encounters more examples, update the database.
    - match the Customer Number field that’s extracted from the image to handle overlapping data writes and updates.
3. Get more data.
    - create a custom image search class using duck-duck-go-search that could quickly take a list of various search terms and advanced settings such as format, region, number of samples, file type filtering, etc... 
    - include standard rate limit handling and error exceptions
    - run the program and download / label
    - collect 10 results for each US State.
    - encapsulate methods to clean and validate the resulting images, 
    - remove any defunct download attempts / broken links 


