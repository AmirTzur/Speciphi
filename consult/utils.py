# OS and DB
import os
from djaroo.settings import BASE_DIR
from django.db import connection, Error
# ML
import numpy as np
import pandas as pd
from sklearn.externals import joblib


class Classifier:
    """

    """
    userClassificationProbs = None
    userMaximalSpecs = None
    userMinimalSpecs = None
    userChosenClusters = None
    modelResults = None
    filteredResults = None
    userAffiliationInput = None
    userAffiliations = None
    brandFilterList = []
    screenSizeFilterList = []
    touchScreenFilterList = []
    screenResolutionFilterList = []
    ramFilterList = []
    gpuFilterList = []
    cpuFilterList = []
    capacityFilterList = []
    operatingSystemFilterList = []
    weightFilterList = [0, float("inf")]
    priceFilterList = [0, float("inf")]

    def __init__(self):
        """

        """
        clusters = None
        models = None
        affiliationMedianUses = None
        try:
            # Clusters
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                cursor.execute('CALL getClusters(%s)', [1])
                clusters = list(cursor)
                clusters = pd.DataFrame.from_records(clusters, columns=[i[0] for i in cursor.description])
                cursor.close()
            # Models List
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                cursor.execute('CALL getLaptopModels()')
                models = list(cursor)
                models = pd.DataFrame.from_records(models, columns=[i[0] for i in cursor.description])
                cursor.close()
            # Affiliation Median Uses
            cursor = connection.cursor()
            if not cursor:
                print("cursor was not defined")
            else:
                cursor.execute('CALL getLaptopAffiliationMedianUse()')
                affiliationMedianUses = list(cursor)
                affiliationMedianUses = pd.DataFrame.from_records(affiliationMedianUses, columns=[i[0] for i in cursor.description])
                cursor.close()
        except Error as e:
            print(e)
        # Random Forest Model
        algo_src = BASE_DIR + '\classifier_algorithm'
        classificationModel = joblib.load(os.path.join(algo_src, 'laptopModel.pkl'))
        # Creating Minimal & Maximal Specs Ranks Summary Table for each Cluster
        ranks = models.ix[:, ['rankCPU', 'rankGPU', 'rankRAM', 'rankHD', 'rankBattery', 'rankWeight', 'clusterId']]
        clustersMinimalSpecs = ranks.groupby(['clusterId'], as_index=False).min()
        clustersMaximalSpecs = ranks.groupby(['clusterId'], as_index=False).max()
        clustersMinimalSpecs.index = clusters.ix[:,1]
        clustersMaximalSpecs.index = clusters.ix[:,1]
        del clustersMinimalSpecs['clusterId']
        del clustersMaximalSpecs['clusterId']
        del [ranks]
        # defaultUserInput
        defaultUserInput = pd.DataFrame([1, 3, 2, 3, 3, 1, 2, 2, 3, 1, 1, 2, 2, 3],
                                        index=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]).T
        # Classification Thresholds
        classificationUpperThreshold = 0.75
        classificationLowerThreshold = 0.125
        # Classifier Attributes
        self.clusters = clusters
        self.classificationModel = classificationModel
        self.listOfmodels = models
        del self.listOfmodels['key']
        self.clustersMaximalSpecs = clustersMaximalSpecs
        self.clustersMinimalSpecs = clustersMinimalSpecs
        self.defaultUserInput = defaultUserInput

        self.classificationUpperThreshold = classificationUpperThreshold
        self.classificationLowerThreshold = classificationLowerThreshold
        self.affiliationMedianUses = affiliationMedianUses
        del self.affiliationMedianUses['cluster']
        self.affiliationMedianUses.index.name = 'cluster'
        self.userApplicationInput = pd.DataFrame(round(affiliationMedianUses.median(axis=0))).T
        self.generateSuitbleResultsAccordingtoUserInput()

    def generateSuitbleResultsAccordingtoUserInput(self):
        """
        Generate results according the user input - Main Function
        :return:
        """
        self.generateClassificationProbs()
        self.generateUserSpecsRange()
        self.findUserClusters()
        self.getResults()
        return (self.filterByRules(self.brandFilterList, self.screenSizeFilterList, self.touchScreenFilterList,
                                   self.screenResolutionFilterList, self.ramFilterList, self.gpuFilterList,
                                   self.cpuFilterList, self.capacityFilterList, self.operatingSystemFilterList,
                                   self.weightFilterList, self.priceFilterList))

    def generateClassificationProbs(self):
        """
        Using the classification model to predict the probs for belonging each cluster - according to the user input - Main Function

        :return:
        """
        userClassificationProbs = self.classificationModel.predict_proba(self.userApplicationInput.ix[:, 0:])
        userClassificationProbs = pd.DataFrame(userClassificationProbs, columns=self.clusters.ix[:,1])

        if (max(userClassificationProbs.ix[0, :]) >= self.classificationUpperThreshold):
            userClassificationProbs.ix[:, userClassificationProbs.ix[0, :] >= self.classificationUpperThreshold] = 1
            userClassificationProbs.ix[:, userClassificationProbs.ix[0, :] < self.classificationUpperThreshold] = 0
        else:
            if (min(userClassificationProbs.ix[0, :]) < self.classificationLowerThreshold):
                userClassificationProbs.ix[:, userClassificationProbs.ix[0, :] < self.classificationLowerThreshold] = 0

        self.userClassificationProbs = pd.DataFrame(
            userClassificationProbs.ix[0, :] / sum(userClassificationProbs.ix[0, :]))

    def generateUserSpecsRange(self):
        """
        Calculating the Weighted Specs Ranks (minimal and maximal) the User Needs
        :return:
        """
        self.userMinimalSpecs = np.matrix(self.userClassificationProbs.ix[:, 0]) * np.matrix(
            self.clustersMinimalSpecs.ix[:, :])
        self.userMaximalSpecs = np.matrix(self.userClassificationProbs.ix[:, 0]) * np.matrix(
            self.clustersMaximalSpecs.ix[:, :])

    def findUserClusters(self):
        """
        find the clusters in which the user belongs to
        :return:
        """
        self.userChosenClusters = pd.DataFrame(self.userClassificationProbs.index.tolist(),
                                               index=self.userClassificationProbs.index) * (
                                      (self.userClassificationProbs > 0) * 1)

    def getResults(self):
        """
        Get suitble models according the user input
        :return:
        """
        self.modelResults = self.listOfmodels.loc[(self.listOfmodels.rankCPU <= self.userMaximalSpecs.item(0))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankGPU <= self.userMaximalSpecs.item(1))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankRAM <= self.userMaximalSpecs.item(2))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankHD <= self.userMaximalSpecs.item(3))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankBattery <= self.userMaximalSpecs.item(4))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankWeight <= self.userMaximalSpecs.item(5))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankCPU >= self.userMinimalSpecs.item(0))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankGPU >= self.userMinimalSpecs.item(1))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankRAM >= self.userMinimalSpecs.item(2))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankHD >= self.userMinimalSpecs.item(3))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankBattery >= self.userMinimalSpecs.item(4))]
        self.modelResults = self.modelResults.loc[(self.modelResults.rankWeight >= self.userMinimalSpecs.item(5))]
        self.modelResults = self.modelResults[self.modelResults['clusterId'].isin(self.userChosenClusters.ix[:, 0])]
        self.modelResults = self.modelResults.drop_duplicates(subset='Model')

    def filterByRules(self, brandFilterList, screenSizeFilterList, touchScreenFilterList, screenResolutionFilterList,
                      ramFilterList, gpuFilterList, cpuFilterList, capacityFilterList, operatingSystemFilterList,
                      weightFilterList, priceFilterList):
        """
        Commit rules for filtering the results
        :param brandFilterList:
        :param screenSizeFilterList:
        :param touchScreenFilterList:
        :param screenResolutionFilterList:
        :param ramFilterList:
        :param gpuFilterList:
        :param cpuFilterList:
        :param capacityFilterList:
        :param operatingSystemFilterList:
        :param weightFilterList:
        :param priceFilterList:
        :return:
        """
        self.initializeFilters()
        self.brandFilterList = brandFilterList
        self.screenSizeFilterList = screenSizeFilterList
        self.touchScreenFilterList = touchScreenFilterList
        self.screenResolutionFilterList = screenResolutionFilterList
        self.ramFilterList = ramFilterList
        self.gpuFilterList = gpuFilterList
        self.cpuFilterList = cpuFilterList
        self.capacityFilterList = capacityFilterList
        self.operatingSystemFilterList = operatingSystemFilterList
        self.weightFilterList = weightFilterList
        self.priceFilterList = priceFilterList
        self.filteredResults = self.modelResults
        self.filteredResults = self.filteredResults.loc[(self.filteredResults.lowestPrice >= self.priceFilterList[0])]
        self.filteredResults = self.filteredResults.loc[(self.filteredResults.lowestPrice <= self.priceFilterList[1])]
        self.filteredResults = self.filteredResults.loc[(self.filteredResults.Weight >= self.weightFilterList[0])]
        self.filteredResults = self.filteredResults.loc[(self.filteredResults.Weight <= self.weightFilterList[1])]
        if (len(self.brandFilterList) != 0):           self.filteredResults = self.filteredResults[
            self.filteredResults['Brand'].isin(brandFilterList)]
        if (len(self.screenSizeFilterList) != 0):      self.filteredResults = self.filteredResults[
            self.filteredResults['Screen.Size'].isin(screenSizeFilterList)]
        if (len(self.touchScreenFilterList) != 0):     self.filteredResults = self.filteredResults[
            self.filteredResults['Touch.Screen'].isin(touchScreenFilterList)]
        if (len(self.screenResolutionFilterList) != 0): self.filteredResults = self.filteredResults[
            self.filteredResults['Screen.Resolution'].isin(screenResolutionFilterList)]
        if (len(self.ramFilterList) != 0):             self.filteredResults = self.filteredResults[
            self.filteredResults['Memory'].isin(ramFilterList)]
        if (len(self.gpuFilterList) != 0):             self.filteredResults = self.filteredResults[
            self.filteredResults['filterGPU'].isin(gpuFilterList)]
        if (len(self.cpuFilterList) != 0):             self.filteredResults = self.filteredResults[
            self.filteredResults['filterCPU'].isin(cpuFilterList)]
        if (len(self.capacityFilterList) != 0):        self.filteredResults = self.filteredResults[
            self.filteredResults['filterCapacity'].isin(capacityFilterList)]
        if (len(self.operatingSystemFilterList) != 0): self.filteredResults = self.filteredResults[
            self.filteredResults['Operating.System'].isin(operatingSystemFilterList)]

        if (len(self.filteredResults) > 3):
            return (self.getTop3Results())
        else:
            return ('Less than 3 Results')

    def getResultsAccordingToAffiliationInput(self, chosenAffiliations):
        """
        Extract Results According to the User Affiliation Choices
        chosenAffiliations = set of current chosen affiliation ex: {1,3,6} such as min=1, max = 8
        :param chosenAffiliations: pd.DataFrame([2,3])
        :return:
        """
        self.initializeFilters()
        if (len(chosenAffiliations) != 0):
            self.userAffiliations = chosenAffiliations
            medianUsesforChosenAffiliations = self.affiliationMedianUses.ix[self.userAffiliations.ix[:, 0], :]
            self.userApplicationInput = pd.DataFrame(medianUsesforChosenAffiliations.max(axis=0)).T
        #
        else:
            self.userAffiliationInput = self.defaultUserInput
        return (self.generateSuitbleResultsAccordingtoUserInput())

    def getResultsAccordingToApplicationInput(self, useId, levelOfUse):
        """
        Extract Results According to the User Application Choices
        :param useId:
        :param levelOfUse: unchecked value = 0
        :return:
        """
        self.initializeFilters()
        self.userApplicationInput.ix[:, useId-1] = levelOfUse
        return (self.generateSuitbleResultsAccordingtoUserInput())

    def getFilterableFeaturesLevels(self):
        """
        get exist levels of filterabled features
        :return:
        """
        filterdResultsLevels = [{"Brand": self.listOfmodels['Brand'].unique().tolist(),
                                 "Screen Size": self.listOfmodels['Screen.Size'].unique().tolist(),
                                 "Touch Screen": self.listOfmodels['Touch.Screen'].unique().tolist(),
                                 "Color": self.listOfmodels['Color'].unique().tolist(),
                                 "Memory": self.listOfmodels['Memory'].unique().tolist(),
                                 "GPU": self.listOfmodels['filterGPU'].unique().tolist(),
                                 "CPU": self.listOfmodels['filterCPU'].unique().tolist(),
                                 "Capacity": self.listOfmodels['filterCapacity'].unique().tolist(),
                                 "Operating System": self.listOfmodels['Operating.System'].unique().tolist()},
                                {"Brand": self.modelResults['Brand'].unique().tolist(),
                                 "Screen Size": self.modelResults['Screen.Size'].unique().tolist(),
                                 "Touch Screen": self.modelResults['Touch.Screen'].unique().tolist(),
                                 "Color": self.modelResults['Color'].unique().tolist(),
                                 "Memory": self.modelResults['Memory'].unique().tolist(),
                                 "GPU": self.modelResults['filterGPU'].unique().tolist(),
                                 "CPU": self.modelResults['filterCPU'].unique().tolist(),
                                 "Capacity": self.modelResults['filterCapacity'].unique().tolist(),
                                 "Operating System": self.modelResults['Operating.System'].unique().tolist()},
                                {"Brand": self.filteredResults['Brand'].unique().tolist(),
                                 "Screen Size": self.filteredResults['Screen.Size'].unique().tolist(),
                                 "Touch Screen": self.filteredResults['Touch.Screen'].unique().tolist(),
                                 "Color": self.filteredResults['Color'].unique().tolist(),
                                 "Memory": self.filteredResults['Memory'].unique().tolist(),
                                 "GPU": self.filteredResults['filterGPU'].unique().tolist(),
                                 "CPU": self.filteredResults['filterCPU'].unique().tolist(),
                                 "Capacity": self.filteredResults['filterCapacity'].unique().tolist(),
                                 "Operating System": self.filteredResults['Operating.System'].unique().tolist()}]
        for sub in filterdResultsLevels:
            for idx, val in enumerate(sub['Memory']): sub['Memory'][idx] = str(val) + 'GB'
            for idx, val in enumerate(sub['Capacity']): sub['Capacity'][idx] = str(val) + 'GB'
            for idx, val in enumerate(sub['Screen Size']): sub['Screen Size'][idx] = str(val) + '"'
        return (filterdResultsLevels)

    def initializeFilters(self):
        """
        Initialize filters
        :return:
        """
        self.brandFilterList = []
        self.screenSizeFilterList = []
        self.touchScreenFilterList = []
        self.screenResolutionFilterList = []
        self.ramFilterList = []
        self.gpuFilterList = []
        self.cpuFilterList = []
        self.capacityFilterList = []
        self.operatingSystemFilterList = []
        self.weightFilterList = [0, float("inf")]

    def getTop3Results(self):
        """
        Find top 3 Results - Best Match, Best Mobility, Best Price
        Using only on first entrance
        :return:
        """
        bestMatch = self.filteredResults.ix[np.argmax(self.filteredResults.overallRank), :]
        bestMatch = self.filteredResults[self.filteredResults['Model'].isin(bestMatch)]
        self.filteredResults = self.filteredResults[-self.filteredResults['Model'].isin(bestMatch['Model'])]
        bestMatch = bestMatch.drop(
            ['clusterId', 'rankCPU', 'rankGPU', 'rankHD', 'rankRAM', 'rankBattery', 'rankWeight', 'dealAmazonRank',
             'lowestPrice', 'filterCapacity', 'filterCPU', 'filterGPU', 'overallRank', 'mobilityRank'], axis=1)

        bestMobility = self.filteredResults.ix[np.argmax(self.filteredResults.mobilityRank), :]
        bestMobility = self.filteredResults[self.filteredResults['Model'].isin(bestMobility)]
        self.filteredResults = self.filteredResults[-self.filteredResults['Model'].isin(bestMobility['Model'])]
        bestMobility = bestMobility.drop(
            ['clusterId', 'rankCPU', 'rankGPU', 'rankHD', 'rankRAM', 'rankBattery', 'rankWeight', 'dealAmazonRank',
             'lowestPrice', 'filterCapacity', 'filterCPU', 'filterGPU', 'overallRank', 'mobilityRank'], axis=1)

        bestPrice = self.filteredResults.ix[np.argmin(self.filteredResults.lowestPrice), :]
        bestPrice = self.filteredResults[self.filteredResults['Model'].isin(bestPrice)]
        self.filteredResults = self.filteredResults[-self.filteredResults['Model'].isin(bestPrice['Model'])]
        bestPrice = bestPrice.drop(
            ['clusterId', 'rankCPU', 'rankGPU', 'rankHD', 'rankRAM', 'rankBattery', 'rankWeight', 'dealAmazonRank',
             'lowestPrice', 'filterCapacity', 'filterCPU', 'filterGPU', 'overallRank', 'mobilityRank'], axis=1)

        top3 = pd.concat([bestMatch, bestMobility, bestPrice])
        top3['sort_indicator'] = ['Best Match', 'Best Mobility', 'Best Price']
        top3 = top3.to_dict('records')
        for sub in top3:
            sub['Memory'] = str(sub['Memory']) + 'GB'
            sub['Screen.Size'] = str(sub['Screen.Size']) + '"'
            sub['Weight'] = str(sub['Weight']) + ' lb.'
            sub['Storage'] = [str(sub['StorageSSD']) + 'GB', str(sub['StorageHDD']) + 'GB']
            del sub['StorageHDD']
            del sub['StorageSSD']
            sub['Screen Size'] = sub.pop('Screen.Size')
            sub['Screen Resolution'] = sub.pop('Screen.Resolution')
            sub['Touch Screen'] = sub.pop('Touch.Screen')
            sub['Operating System'] = sub.pop('Operating.System')

        return top3

    def getRecommendedSpecification(self):
        """
        Return Our Recommended Specification
        :return:
        """

        return ()

