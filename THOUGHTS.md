1. How would your design change if the data was not static (i.e updated frequently
during the day)?
* There would need to be functionality to update the stored data with changes
* Would want to make the request non cacheable so changes in data are retrieved
* The actual request logic would not need to be changed

2. Do you think your design can handle 1000 concurrent requests per second? If not, what
would you change?
* Profiling current performance indicates a single request takes ~0.8 seconds to respond and most of that time is spent querying the database
* Handling concurrent requests would put further load on the database. I'm not sure exactly how this would scale in SQLite - would need to do some testing with concurrent requests to investigate. It seems unlikely that it would handle 1000 concurrent requests per second without response time slowing significantly.
* I would want to do a more detailed profiling of the requests to see what specific factors are limiting the database query (e.g. IO, CPU, Memory)
* Below are some things I would investigate to see if they can be changed to improve performance:
  * Changing the deployment model:
    * Storing the data on a separate physical disk to isolate IO
    * Deploying the application on more powerful hardware, or in a distributed set of servers to enable load to be spread across the nodes
    * Partitioning the data (perhaps by location, or tags?) so that individual requests can be handled by separate disks, reducing contention
  * Look into external database/search products recognised for performance capabilities (e.g. Elasticsearch) to replace use of SQLite
  * Consider whether an in-memory data storage would be appropriate - it would be suitable for this small volume of data but may not be appropriate if the solution needs to be used with larger data volumes
