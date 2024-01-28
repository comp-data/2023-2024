# Data Science: project

The goal of the project is to develop a software that enables one to process data stored in different formats and to upload them into two distinct databases to query these databases simultaneously according to predefined operations. 

## Data

Exemplar data for testing the project have been made available. In particular:

* for creating the relational database, there is one file, [a JSON file](data/process.json) containing information of the process of acquisition and digitisation of a cultural heritage object, which passes through five distinct activities: acquisiting, processing, modelling, optimising, exporting. The cultural heritage object is indentified by the attribute `object id`, which correspond to the identifier of the object the metadata file (see below).

* for creating the graph database, there is two one, [a CSV file](data/meta.csv), containing metadata about cultural heritage objects. Please note that multiple authors of the same object will be contained in just one string and split by `; `. In addition, the value between curvy brackets is not part of the name but it is the identifier for that person - meaning that multiple mentions of such identifiers in different rows refer always to the same person.



## Workflow

![Workflow of the project](img/workflow.png)

## Data model

![Data model](img/datamodel.png)

## UML of data model classes

![Data model classes](img/datamodel-uml.png)

All the methods of each class must return the appropriate value that have been specified in the object of that class when it has been created. It is up to the implementer to decide how to enable someone to add this information to the object of each class, e.g. by defining a specific constructor. While one can add additional methods to each class if needed, it is crucial that the *get* methods introduced in the UML diagram are all defined.

## UML of additional classes

![Data model classes](img/classes-uml.png)

All the attributes methods of each class are defined as follows. All the constructors of each of the class introduced in the UML diagram do not take in input any parameter. While one can add additional methods to each class if needed, it is crucial that all the methods introduced in the UML diagram are defined.


### Class `Handler`

#### Attributes
`dbPathOrUrl`: the variable containing the path or the URL of the database, initially set as an empty string, that will be updated with the method `setDbPathOrUrl`.

#### Methods
`getDbPathOrUrl`: it returns the path or URL of the database.

`setDbPathOrUrl`: it enables to set a new path or URL for the database to handle.


### Class `UploadHandler`

#### Methods
`pushDataToDb`: it takes in input the path of a file containing annotations and uploads them in the database. This method can be called everytime there is a need to upload annotations in the database. The actual implementation of this method is left to its subclasses.


### Classes `MetadataUploadHandler` and `ProcessDataUploadHandler`

These two classes implements the method of the superclass to handle the specific scenario, i.e. `MetadataUploadHandler` to handle CSV files in input and to store their data in a graph database and `ProcessDataUploadHandler` to handle JSON files in input and to store their data in a relational database.


### Class `QueryHandler`

#### Methods
`getById`: it returns a data frame with all the entities matching the input identifier (i.e. maximum one entity if there exists one with the input id).


### Class `MetadataQueryHandler`

#### Methods
`getAllPeople`: it returns a data frame containing all the people included in the database.

`getAllCulturalHeritageObjects`: it returns a data frame with all the cultural heritage objects described in it.

`getAuthorsOfCulturalHeritageObject`: it returns a data frame with all the authors of the cultural heritage objects identified by the input id.

`getCulturalHeritageObjectsAuthoredBy`: it returns a data frame with all the cultural heritage objects authored by the person identified by the input id.


### Class `ProcessDataQueryHandler`

#### Methods
`getAllActivities`: it returns a data frame with all the activities included in the database.

`getActivitiesByResponsibleInstitution`: it returns a data frame with all the activities that have, as responsible institution, any that matches (even partially) with the input string.

`getActivitiesByResponsiblePerson`: it returns a data frame with all the activities that have, as responsible person, any that matches (even partially) with the input string.

`getActivitiesUsingTool`: it returns a data frame with all the activities that have, as a tool used, any that matches (even partially) with the input string.

`getActivitiesStartedAfter`: it returns a data frame with all the activities that started either exactly on or after the date specified as input.

`getActivitiesEndedBefore`: it returns a data frame with all the activities that ended either exactly on or before the date specified as input.

`getAcquisitionsByTechnique`: it returns a data frame with all the acquisitions that have, as a technique used, any that matches (even partially) with the input string.



### Class `BasicMashup`

#### Attributes
`metadataQuery`: the variable containing the list of `MetadataQueryHandler` objects to involve when one of the *get* methods below (needing metadata) is executed. In practice, every time a *get* method is executed, the method will call the related method on all the `MetadataQueryHandler` objects included in the variable `metadataQuery`, before combining the results with those of other `QueryHandler`(s) and returning the requested object.

`processQuery`: the variable containing the list of `ProcessorDataQueryHandler` objects to involve when one of the *get* methods below (needing acquisition and digitisation information) is executed. In practice, every time a *get* method is executed, the method will call the related method on all the `ProcessorDataQueryHandler` objects included in the variable `processQuery`, before combining the results with those of other `QueryHandler`(s) and returning the requested object.


#### Methods
`cleanMetadataHandlers`: it cleans the list `metadataQuery` from all the `MetadataQueryHandler` objects it includes.

`cleanProcessHandlers`: it cleans the list `processQuery` from all the `ProcessorDataQueryHandler` objects it includes.

`addMetadataHandler`: it appends the input `MetadataQueryHandler` object to the list `metadataQuery`.

`addProcessHandler`: it appends the input `ProcessorDataQueryHandler` object to the list `processQuery`.

`getEntityById`: it returns an object having class `IdentifiableEntity` identifying the entity available in the databases accessible via the query handlers matching the input identifier (i.e. maximum one entity). In case no entity is identified by the input identifier, `None` must be returned. The object returned must belong to the appropriate class – e.g. if the `IdentifiableEntity` to return is actually a person, an instance of the class `Person` (being it a subclass of `IdentifiableEntity`) must be returned.

`getAllPeople`: it returns a list of objects having class `Person` containing all the people included in the database accessible via the query handlers.

`getAllCulturalHeritageObjects` it returns a list of objects having class `CulturalHeritageObject` containing all the people included in the database accessible via the query handlers. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.

`getAuthorsOfCulturalHeritageObject`: it returns a list of objects having class `Person` with all the authors of the cultural heritage objects identified by the input id.

`getCulturalHeritageObjectsAuthoredBy`: it returns a list of objects having class `CulturalHeritageObjects` with all the cultural heritage objects authored by the person identified by the input id. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.

`getAllActivities`: it returns a list of objects having class `Activity` with all the activities included in the database. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getActivitiesByResponsibleInstitution`: it returns a list of objects having class `Activity` with all the activities that have, as responsible institution, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getActivitiesByResponsiblePerson`: it returns a list of objects having class `Activity` with all the activities that have, as responsible person, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getActivitiesUsingTool`: it returns a list of objects having class `Activity` with all the activities that have, as a tool used, any that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getActivitiesStartedAfter`: it returns a list of objects having class `Activity` with all the activities that started either exactly on or after the date specified as input. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getActivitiesEndedBefore`: it returns a list of objects having class `Activity` with all the activities that ended either exactly on or before the date specified as input. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getAcquisitionsByTechnique`: it returns a list of objects having class `Acquisition` with all the acquisitions that have, as a technique used, any that matches (even partially) with the input string.



### Class `AdvancedMashup`


#### Methods
`getActivitiesOnObjectsAuthoredBy`: it returns a list of objects having class `Activity` referring to the cultural heritage objects authored by the person specified by the input identifier. The objects included in the list must belong to the appropriate class – e.g. if the `Activity` to return is actually an optimising activity, an instance of the class `Optimising` (being it a subclass of `Activity`) must be returned.

`getObjectsHandledByResponsiblePerson`: it returns a list of objects having class `CulturalHeritageObject` with all the cultural heritage objects involved in any activity handled by the responsible person that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.

`getObjectsHandledByResponsibleInstitution`: it returns a list of objects having class `CulturalHeritageObject` with all the cultural heritage objects involved in any activity handled by the responsible institution that matches (even partially) with the input string. The objects included in the list must belong to the appropriate class – e.g. if the `CulturalHeritageObject` to return is actually a map, an instance of the class `Map` (being it a subclass of `CulturalHeritageObject`) must be returned.

`getAuthorsOfObjectsAcquiredInTimeFrame`: it returns a list of objects having class `Person` of the authors of the cultural heritage objects that have been fully acquired in the time window provided as input.



## Uses of the classes

```
# Supposing that all the classes developed for the project
# are contained in the file 'impl.py', then:

# 1) Importing all the classes for handling the relational database
from impl import ProcessDataUploadHandler, ProcessDataQueryHandler

# 2) Importing all the classes for handling graph database
from impl import MetadataUploadHandler, MetadataQueryHandler

# 3) Importing the class for dealing with mashup queries
from impl import AdvancedMashup

# Once all the classes are imported, first create the relational
# database using the related source data
rel_path = "relational.db"
process = ProcessDataUploadHandler()
process.setDbPathOrUrl(rel_path)
process.pushDataToDb("data/process.json")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# Then, create the graph database (remember first to run the
# Blazegraph instance) using the related source data
grp_endpoint = "http://127.0.0.1:9999/blazegraph/sparql"
metadata = MetadataUploadHandler()
metadata.setDbPathOrUrl(grp_endpoint)
metadata.pushDataToDb("data/meta.csv")
# Please remember that one could, in principle, push one or more files
# calling the method one or more times (even calling the method twice
# specifying the same file!)

# In the next passage, create the query handlers for both
# the databases, using the related classes
process_qh = ProcessDataQueryHandler()
process_qh.setDbPathOrUrl(rel_path)

metadata_qh = MetadataQueryHandler()
metadata_qh.setDbPathOrUrl(grp_endpoint)

# Finally, create a advanced mashup object for asking
# about data
mashup = AdvancedMashup()
mashup.addProcessHandler(process_qh)
mashup.addMetadataHandler(metadata_qh)

result_q1 = mashup.getAllActivities()
result_q2 = mashup.getAuthorsOfCulturalHeritageObject("1")
result_q3 = mashup.getAuthorsOfObjectsAcquiredInTimeFrame("2023-04-01", "2023-05-01")
# etc...
```

## Submission of the project

You have to provide all Python files implementing your project, by sharing them in some way (e.g. via OneDrive). You have to send all the files **two days before** the exam session you want to take. Before submitting the project, you must be sure that your code passes a basic test which aims at checking if the code is runnable and compliant with the specification of the UML. The test will be provide in the next weeks.
