from pyspark.sql import SparkSession
from pyspark import SparkContext
from pyspark.sql.functions import sha2, concat_ws
import sys

def main():
    spark = SparkSession.builder.appName("Anonymize PySpark").getOrCreate()
    args_iter = iter(sys.argv[1:])
    args = dict(zip(args_iter, args_iter))
    
    #sample args for interactive testing
    #args = {'project_bucket': 'project1-lz', 'input_table': 'upload', 'output_table': 'raw', 'database': 'default', 'file_name': 'Tweets.csv'}

    project_bucket = args['project_bucket']
    input_table = args['input_table']
    output_table = args['output_table']
    database = args['database']
    input_s3_uri = 's3://' + project_bucket + '/' + input_table + '/' + args['file_name']
    output_s3_uri = 's3://' + project_bucket + '/' + output_table + '/' + args['file_name'].split('.')[0] + '-anon/'

    # Interactive pyspark from glue development endpoint allows reaading from glue crawlers
    # from awsglue.context import GlueContext
    #glueContext = GlueContext(SparkContext.getOrCreate())

    # Create a dataframe from glue catalog
    #df = glueContext.create_data_frame.from_catalog(database=database, table_name=input_table)

    #Print out information about this data
    #print("Count:  ", df.count())
    #df.printSchema()

    df = spark.read.csv(input_s3_uri, header=True)

    # replace each tweeters name with crc bigint
    dfAnnocrc = df.withColumn("annonym", sha2("name", 256)).select("annonym", "tweet_id", "airline", "airline_sentiment", "text")

    # write back to s3 as parquet
    dfAnnocrc.write.mode("append").parquet(output_s3_uri)



if __name__ == "__main__":
    main()




