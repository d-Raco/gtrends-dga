# gtrends-dga
 Domain Generation Algorithm developed with Google Trends

 To give some context, DGAs (Domain Generation Algorithms) are used by cybercriminals who, when deploying a botnet around the world, need a way to communicate with them. To do this, they use servers called Command & Control (C2 / C&C). In order for the bots to know where this server is, the cybercriminals assign them a domain name. Since this domain name is easily blocked by LEAs (Law Enforcement Agencies), DGAs were created to dynamically set up domains on a daily or even hourly basis so that all bots can generate this domain name on their own and connect to it.


## Problems to overcome

 I have already mentioned some of the problems and restrictions that a DGA tries to overcome, but I think it is interesting to list them here in order to set our priorities while developing the algorithm so that we can keep a clear focus on the problem itself:

- Servers are expensive, but DNS domains are cheap.
- Avoid take-downs by dynamically registering different DNS domains.
- Avoid take-downs by having a large enough DNS domain pool.
- Use non-predictive generation algorithms, since the algorithm can be obtained or inferred.
- Machine learning can detect abnormal domain names; DNS domains must be human readable.
- The generated domain may not already be registered, so the algorithm must generate domains until one is registered.

## DGA development

### Dictionary

 The first step is to create the domain name pool. As previously stated, it must be large and human readable. The best way to do both is to gather words into a list and combine them to form readable domains that have a large number of possible combinations. In my case, I started from [this](https://github.com/baderj/domain_generation_algorithms/blob/master/nymaim2/words.json) DGA word dictionary.

 The idea of that DGA is to create a domain following the syntax shown bellow, where _word_ is retrieved from a list of hard-coded words, _separator_ is either '-' or '' and _tld_ is retrieved from a list of hard-coded TLDs (Top Level Domains). Some examples would be:

 ![syntax1](/img/syntax1.png)

 I like the idea, but some of the generated domains can be strange. In order to make it more believable, I decided to refine the syntax to a more grammatically accurate one:

 ![syntax2](/img/syntax2.png)

 At first, I created the largest dictionary I could, so that the domain pool would be as large possible, thus ensuring protection against take-downs. I gathered _4.840_ [adjectives](https://patternbasedwriting.com/elementary_writing_success/list-4800-adjectives/) and _11.061_ [nouns](https://greenopolis.com/list-of-nouns/). Having _2_ possible separators and _70_ TLDs, the total number of potential domain names is _7.494.933.600_.

 The problem with having such a large list of adjectives and nouns is that some of them are not commonly used, making the domain easily detectable. For this reason, I created another dictionary with only the _100_ most common [adjectives](https://www.espressoenglish.net/100-common-adjectives-in-english/) and [nouns](https://www.espressoenglish.net/100-common-nouns-in-english/), and the _16_ most common TLDs, adding to a total of _320.000_ different possible domain names. Some examples:

 ![dictionaries](/img/dictionaries.png)

 The full dictionary has a larger number of DNS domains available (almost _100%_, since I have not encountered any registered domain when using this dictionary) while the common dictionary has almost _90%_ of domain availability, as _1_ out of _10_ domains generated with this dictionary appear to be already registered. The difference in storage space occupied by each of them should also be considered: the full dictionary takes up _316.8KB_ while the common dictionary only _3.8KB_.

 In the end, I decided to keep both dictionaries, as they serve different purposes.

### Algorithm
 The next step is to think of a publicly available non-predictive seed for all devices that even the hosting server cannot predict or decide. Additionally, it should be easily integrated into the algorithm code and its collection should not be slow.

 After some consideration, three online resources met these requirements: _Twitter's trending topic_, _Spotify's Top Hits_ and _Google Trends_. The reason I chose them is that they all have Python APIs and even the companies themselves cannot predict their future values.

 I discarded both Twitter and Spotify, since their APIs need account credentials, which implies that if the account is banned, the whole algorithm becomes useless. In contrast, no credentials are needed to access Google Trends, which makes it the more robust option. For this reason, I will use _pytrends_ (Google Trends' Python API).

 Pytrends _trending_searches()_ method returns the 20 most [trending Google searches](https://trends.google.com/trends/trendingsearches/daily?geo=US) in the US. Using the _pandas_ library, the result can be stored in a data frame.

 ![Google Trends](/img/GoogleTrends.png)

 Now, the next step is to transform these results into an index to pick words from the dictionary. This can be done by hashing the trend using md5 and then converting the hash from hexadecimal to integer. To change the domain generated every hour, I decided to concatenate the year, month, day and hour to the trend before hashing. I also concatenate a modifier, which will be discussed later. Then, this number is used as an index for the dictionary.

 The adjective, separator, noun and TLD used for the domain will be the resulting element whose position of each list type is equal to "index % size of list". For example:

 ![example](/img/example.png)

 Now, to add a little more randomness, I decided to select just one of the twenty Google Trends. To choose which one, a hard-coded hexadecimal seed is concatenated with the year, month, day, hour and modifier and then hashed. This hash is then transformed into an integer and the modulus of this integer divided by twenty (the number of Google Trends results) is the trend that will be used.

 ![algorithm](/img/algorithm.png)

 The modifier is used if the generated domain is not registered. In that case, the value of the modifier, which starts at _0_, is incremented by _1_ at each attempt until a registered domain is found. For this, I also had to implement a function to check if a connection to the domain could be performed successfully.

 Finally, the domain is printed. When deployed, this algorithm should be called at specific time intervals so that each bot generates a domain at the same specific time (hourly, every 3 hours, daily, etc.). All the code can be found in [this](https://github.com/Rymond3/gtrends-dga) Github repository.
