# -*- coding: utf-8 -*-
# Copyright (c) 2023, Silvio Peroni <essepuntato@gmail.com>
#
# Permission to use, copy, modify, and/or distribute this software for any purpose
# with or without fee is hereby granted, provided that the above copyright notice
# and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND
# FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT,
# OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE,
# DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
# ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS
# SOFTWARE.
import unittest
from os import sep
from pandas import DataFrame
from impl import MetadataUploadHandler, ProcessDataUploadHandler
from impl import MetadataQueryHandler, ProcessDataQueryHandler
from impl import AdvancedMashup
from impl import Person, CulturalHeritageObject, Activity, Acquisition

# REMEMBER: before launching the tests, please run the Blazegraph instance!

class TestProjectBasic(unittest.TestCase):

    # The paths of the files used in the test should change depending on what you want to use
    # and the folder where they are. Instead, for the graph database, the URL to talk with
    # the SPARQL endpoint must be updated depending on how you launch it - currently, it is
    # specified the URL introduced during the course, which is the one used for a standard
    # launch of the database.
    metadata = "data" + sep + "meta.csv"
    process = "data" + sep + "process.json"
    relational = "." + sep + "relational.db"
    graph = "http://127.0.0.1:9999/blazegraph/sparql"
    
    def test_01_MetadataUploadHandler(self):
        u = MetadataUploadHandler()
        self.assertTrue(u.setDbPathOrUrl(self.graph))
        self.assertEqual(u.getDbPathOrUrl(), self.graph)
        self.assertTrue(u.pushDataToDb(self.metadata))

    def test_02_ProcessDataUploadHandler(self):
        u = ProcessDataUploadHandler()
        self.assertTrue(u.setDbPathOrUrl(self.relational))
        self.assertEqual(u.getDbPathOrUrl(), self.relational)
        self.assertTrue(u.pushDataToDb(self.process))
    
    def test_03_MetadataQueryHandler(self):
        q = MetadataQueryHandler()
        self.assertTrue(q.setDbPathOrUrl(self.graph))
        self.assertEqual(q.getDbPathOrUrl(), self.graph)

        self.assertIsInstance(q.getById("just_a_test"), DataFrame)

        self.assertIsInstance(q.getAllPeople(), DataFrame)
        self.assertIsInstance(q.getAllCulturalHeritageObjects(), DataFrame)
        self.assertIsInstance(q.getAuthorsOfCulturalHeritageObject("just_a_test"), DataFrame)
        self.assertIsInstance(q.getCulturalHeritageObjectsAuthoredBy(
            "just_a_test"), DataFrame)
    
    def test_04_ProcessDataQueryHandler(self):
        q = ProcessDataQueryHandler()
        self.assertTrue(q.setDbPathOrUrl(self.relational))
        self.assertEqual(q.getDbPathOrUrl(), self.relational)

        self.assertIsInstance(q.getById("just_a_test"), DataFrame)

        self.assertIsInstance(q.getAllActivities(), DataFrame)
        self.assertIsInstance(q.getActivitiesByResponsibleInstitution(
            "just_a_test"), DataFrame)
        self.assertIsInstance(q.getActivitiesByResponsiblePerson("just_a_test"), DataFrame)
        self.assertIsInstance(q.getActivitiesUsingTool("just_a_test"), DataFrame)
        self.assertIsInstance(q.getActivitiesStartedAfter("1088-01-01"), DataFrame)
        self.assertIsInstance(q.getActivitiesEndedBefore("2029-01-01"), DataFrame)
        self.assertIsInstance(q.getAcquisitionsByTechnique("just_a_test"), DataFrame)
        
    def test_05_AdvancedMashup(self):
        qm = MetadataQueryHandler()
        qm.setDbPathOrUrl(self.graph)
        qp = ProcessDataQueryHandler()
        qp.setDbPathOrUrl(self.relational)

        am = AdvancedMashup()
        self.assertIsInstance(am.cleanMetadataHandlers(), bool)
        self.assertIsInstance(am.cleanProcessHandlers(), bool)
        self.assertTrue(am.addMetadataHandler(qm))
        self.assertTrue(am.addProcessHandler(qp))

        self.assertEqual(am.getEntityById("just_a_test"), None)

        r = am.getAllPeople()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Person)

        r = am.getAllCulturalHeritageObjects()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, CulturalHeritageObject)

        r = am.getAuthorsOfCulturalHeritageObject("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Person)

        r = am.getCulturalHeritageObjectsAuthoredBy("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, CulturalHeritageObject)

        r = am.getAllActivities()
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getActivitiesByResponsibleInstitution("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getActivitiesByResponsiblePerson("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getActivitiesUsingTool("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getActivitiesStartedAfter("1088-01-01")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getActivitiesEndedBefore("2029-01-01")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getAcquisitionsByTechnique("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Acquisition)

        r = am.getActivitiesOnObjectsAuthoredBy("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Activity)

        r = am.getObjectsHandledByResponsiblePerson("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, CulturalHeritageObject)

        r = am.getObjectsHandledByResponsibleInstitution("just_a_test")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, CulturalHeritageObject)

        r = am.getAuthorsOfObjectsAcquiredInTimeFrame("1088-01-01", "2029-01-01")
        self.assertIsInstance(r, list)
        for i in r:
            self.assertIsInstance(i, Person)   
