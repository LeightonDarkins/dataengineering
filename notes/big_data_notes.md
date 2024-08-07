# Big Data

## Key Characteristics

- Volume: Designed to handle extremely high volumes of data.
- Variety: Data spans a vast variety of structures.
- Velocity: Capable of processing data extremely quickly.

## Evolution of Big Data technologies

### Googles first Products in this space

- Google File System (GFS): Distributed filesystem.
- Google Map Reduce
- Google BigTable: Distributed Index Table.

### Hadoop

- HDFS: Hadoop Distributed Filesystem
- Hadoop Map Reduce
- HBase
- Sqoop (retired)
- Hive (retired)
- Flume
- Oozie

Steep learning curve, expensive to set up and run, inefficient with memory and slower than newer approaches.

### Spark solves for those ^^ issues

## Modern Data Lakes on the Cloud

Sources are RDBMSs and Log/Plaintext files.

Concepts include:

- Object Storage (S3)
    - Streaming Ingestion
    - Batch Ingestion
- Distributed Compute
- Orchestration

## Data Processing concepts

- Sources
    - Files
    - Purpose Built DBs
    - REST Payloads
    - Streaming Technologies (Kafka etc.)
- Processing
    - ETL Tools
    - Libraries (pandas etc.)
        - pandas
        - Dask
        - PySpark
    - Frameworks (Spark, Hadoop)
- Targets/Sinks
    - Files
    - Data Warehouses/Lakes
    - REST Payloads
    - Streaming Technologies (Kafka etc.)

## Data Processing Libraries/Frameworks

- Pandas
    - lightweight, easy to learn, easy to set up, suited for low volume use-cases, anyone with an interest in Data should use this.
- Dask
    - Extends on Pandas capabilities, easy to learn, can be hard to configure, low-moderate use-cases, good for data scientists
PySpark
    - Intended for distributed use, easy to learn, complex to configure, high volume use-cases, Data Engineers should use this.

## Spark

### Infrastrutcture

- Spark Cluster
    - Master: Manage Clusters
    - Drivers: Submit work
    - Workers: Process the Data

1 or 2 Drivers, 1 or 2 Masters, N number of Workers

Cluster Managers:

- Spark Native / Stand Alone (widely used in Databricks)
- YARN (AWS, GCP, Azure)
- Kubernetes (self hosted)
- Mesos (deprecated)

Executors on Workers: Spark Runtime where work will be done (JVM for example).
Executors have 4 Slots or 4 units of capacity available when the Worker starts.
Slots convert into Tasks when work needs to be done, once the work is done theyt turn back into a Slot.






