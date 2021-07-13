class HashController:
    def __init__(self, CC, hashFieldTable, hashTree):
        self.__CC = CC
        self.__IC = 1 - self.__CC
        self.__hashFieldTable = hashFieldTable
        self.__hashTree = hashTree

    def calcHashScore(self):

        # Calc estimation scores
        for i in range(0, self.__hashFieldTable.size):
            self.__hashFieldTable["Cost"][i] = self.__hashTree[
                self.__tagPopularity.loc[i][0]
            ]

        self.__hashFieldTable["Score"] = (
            self.__CC * self.__hashFieldTable["Number of Posts"]
            + self.__IC * self.__hashFieldTable["Cost"]
        )

    def gradEstim(self):
        pass

    def calcControl(self):
        pass
