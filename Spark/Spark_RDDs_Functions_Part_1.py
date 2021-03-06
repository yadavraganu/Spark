#!/usr/bin/env python
# coding: utf-8

# In[1]:


from pyspark.sql import SparkSession


# In[2]:


spark=SparkSession.builder.appName("RDD Trasformation & Actions").getOrCreate()


# In[6]:


# MAP Return a new RDD by applying a function to each element of this RDD
x = spark.sparkContext.parallelize(["b", "a", "c"])
y = x.map(lambda z: (z, 1))
print(x.collect())
print(y.collect())


# In[7]:


# Filter Return a new RDD containing only the elements that satisfy a predicate
x = spark.sparkContext.parallelize([1,2,3])
y = x.filter(lambda x: x%2 == 0) #keep even values
print(x.collect())
print(y.collect())


# In[8]:


# FlatMap Return a new RDD by first applying a function to all elements of this RDD, and then flattening the results
x = spark.sparkContext.parallelize([1,2,3])
y = x.flatMap(lambda x: (x, x*100, 42))
print(x.collect())
print(y.collect())


# In[14]:


#Group By Group the data in the original RDD. Create pairs where the key is the output of
# a user function, and the value is all items for which the function yields this key.
x = spark.sparkContext.parallelize(['John', 'Fred', 'Anna', 'James'])
y = x.groupBy(lambda w: w[0])
print([(k, list(v)) for (k, v) in y.collect()])


# In[16]:


# Group By Key  Group the values for each key in the original RDD. Create a new pair where the
# original key corresponds to this collected group of values.
x = spark.sparkContext.parallelize([('B',5),('B',4),('A',3),('A',2),('A',1)])
y = x.groupByKey()
print(x.collect())
print(list((j[0], list(j[1])) for j in y.collect()))


# In[20]:


#MapPartitions Return a new RDD by applying a function to each partition of this RDD
x = spark.sparkContext.parallelize([1,2,3], 2)
def f(iterator): yield sum(iterator); yield 42
y = x.mapPartitions(f)
# glom() flattens elements on the same partition
print(x.glom().collect())
print(y.glom().collect())


# In[21]:


#Return a new RDD by applying a function to each partition of this RDD,
#while tracking the index of the original partition
x = spark.sparkContext.parallelize([1,2,3], 2)
def f(partitionIndex, iterator): yield (partitionIndex, sum(iterator))
y = x.mapPartitionsWithIndex(f)
# glom() flattens elements on the same partition
print(x.glom().collect())
print(y.glom().collect())


# In[44]:


# sample Return a new RDD containing a statistical sample of the original RDD
x = spark.sparkContext.parallelize([1, 2, 3, 4, 5])
y = x.sample(False,.4,42)
print(x.collect())
print(y.collect())


# In[46]:


#Union Return a new RDD containing all items from two original RDDs. Duplicates are not culled.
x = spark.sparkContext.parallelize([1,2,3], 2)
y = spark.sparkContext.parallelize([3,4], 2)
z = x.union(y)
print(z.glom().collect())


# In[48]:


# Join Return a new RDD containing all pairs of elements having the same key in the original RDDs
x = spark.sparkContext.parallelize([("a", 1), ("b", 2)])
y = spark.sparkContext.parallelize([("a", 3), ("a", 4), ("b", 5)])
z = x.join(y)
print(z.collect())


# In[49]:


# distinct Return a new RDD containing distinct items from the original RDD (omitting all duplicates)
x = spark.sparkContext.parallelize([1,2,3,3,4])
y = x.distinct()
print(y.collect())


# In[50]:


#coalesce Return a new RDD which is reduced to a smaller number of partitions
x = spark.sparkContext.parallelize([1, 2, 3, 4, 5], 3)
y = x.coalesce(2)
print(x.glom().collect())
print(y.glom().collect())


# In[52]:


# Key BY Create a Pair RDD, forming one pair for each item in the original RDD. The
# pair’s key is calculated from the value via a user-supplied function.
x = spark.sparkContext.parallelize(['John', 'Fred', 'Anna', 'James'])
y = x.keyBy(lambda w: w[0])
print(y.collect())


# In[54]:


#Return a new RDD with the specified number of partitions, placing original
#items into the partition returned by a user supplied function
x = spark.sparkContext.parallelize([('J','James'),('F','Fred'),('A','Anna'),('J','John')], 3)
y = x.partitionBy(2, lambda w: 0 if w[0] < 'H' else 1)
print(x.glom().collect())
print(y.glom().collect())


# In[55]:


# zip Return a new RDD containing pairs whose key is the item in the original RDD, and whose
#value is that item’s corresponding element (same partition, same index) in a second RDD
x = spark.sparkContext.parallelize([1, 2, 3])
y = x.map(lambda n:n*n)
z = x.zip(y)
print(z.collect())


# In[58]:


#getNumPartitions Return the number of partitions in RDD
x = spark.sparkContext.parallelize([1,2,3], 2)
y = x.getNumPartitions()
print(x.glom().collect())
print(y)


# In[59]:


# collect Return all items in the RDD to the driver in a single list
x = spark.sparkContext.parallelize([1,2,3], 2)
y = x.collect()
print(x.glom().collect())
print(y)


# In[60]:


# reduce Aggregate all the elements of the RDD by applying a user function
# pairwise to elements and partial results, and returns a result to the driver
x = spark.sparkContext.parallelize([1,2,3,4])
y = x.reduce(lambda a,b: a+b)
print(x.collect())
print(y)


# In[61]:


#Aggregate all the elements of the RDD by:
#- applying a user function to combine elements with user-supplied objects,
#- then combining those user-defined results via a second user function,
#- and finally returning a result to the driver.

seqOp = lambda data, item: (data[0] + [item], data[1] + item)
combOp = lambda d1, d2: (d1[0] + d2[0], d1[1] + d2[1])
x = spark.sparkContext.parallelize([1,2,3,4])
y = x.aggregate(([], 0), seqOp, combOp)
print(y)


# In[62]:


#Max Return the maximum item in the RDD
x = spark.sparkContext.parallelize([2,4,1])
y = x.max()
print(x.collect())
print(y)


# In[63]:


#Return the sum of the items in the RDD
x = spark.sparkContext.parallelize([2,4,1])
y = x.sum()
print(x.collect())
print(y)


# In[64]:


# Mean Return the mean of the items in the RDD
x = spark.sparkContext.parallelize([2,4,1])
y = x.mean()
print(x.collect())
print(y)


# In[65]:


# stdev Return the standard deviation of the items in the RDD
x = spark.sparkContext.parallelize([2,4,1])
y = x.stdev()
print(x.collect())
print(y)


# In[66]:


# countByKey Return a map of keys and counts of their occurrences in the RDD
x = spark.sparkContext.parallelize([('J', 'James'), ('F','Fred'),
('A','Anna'), ('J','John')])
y = x.countByKey()
print(y)


# In[14]:


# Interoperating Between DataFrames, Datasets, and RDDs
spark.range(10).rdd.glom().collect()
spark.range(10).toDF("id").rdd.map(lambda row: row[0]).collect()
spark.range(10).rdd.toDF().show()


# In[15]:


# Give name to RDD to monitor in Spark GUI
myCollection = "Spark The Definitive Guide : Big Data Processing Made Simple".split(" ")
words = spark.sparkContext.parallelize(myCollection, 2)
words.setName("myWords")
words.name()


# In[23]:


#This creates an RDD for which each record in the RDD represents a line in that text file or files.
current_dir=os.getcwd()
full_path=os.path.join(current_dir,'data','netflix_titles.csv')
data=spark.sparkContext.textFile(full_path)
data.take(2)


# In[29]:


#Alternatively, you can read in data for which each text file should become a single record. 
spark.sparkContext.wholeTextFiles(full_path).take(1)


# In[30]:


#sort
words.sortBy(lambda word: len(word) * -1).take(2)


# In[31]:


#reduce
spark.sparkContext.parallelize(range(1, 5)).reduce(lambda x, y: x + y)


# In[32]:


#count
words.count()


# In[33]:


#countapprox
confidence = 0.95
timeoutMilliseconds = 400
words.countApprox(timeoutMilliseconds, confidence)


# In[34]:


#The same principles apply for caching RDDs as for DataFrames and Datasets.
words.cache()
#We can specify a storage level as any of the storage levels in the singleton object
words.getStorageLevel()


# In[35]:


#Checkpointing
#is the act of saving an RDD to disk so that future references to this RDD point to those
#intermediate partitions on disk rather than recomputing the RDD from its original source. This is
#similar to caching except that it’s not stored in memory, only disk
spark.sparkContext.setCheckpointDir(current_dir)
words.checkpoint()


# In[44]:


#mapPartitions - this means that we operate on a per-partition basis and allows us to perform an
#operation on that entire partition
words.glom().collect()
words.mapPartitions(lambda part: [1]).glom().collect()


# In[46]:


#Other functions similar to mapPartitions include mapPartitionsWithIndex. With this you
#specify a function that accepts an index (within the partition) and an iterator that goes through all
#items within the partition.
def indexedFunc(partitionIndex, withinPartIterator):
    return ["partition: {} => {}".format(partitionIndex,
x) for x in withinPartIterator]
words.mapPartitionsWithIndex(indexedFunc).collect()


# In[48]:


#Although mapPartitions needs a return value to work properly, this next function does not.
#foreachPartition simply iterates over all the partitions of the data.
def f(iterator):
    for x in iterator:
         print(x)
words.foreachPartition(f)

