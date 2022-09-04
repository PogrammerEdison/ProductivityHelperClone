import main 
import excelLinearConverter
from main import write

def converterTest():
    file = open('testExcelText.txt','r')
    testLines = file.readlines()
    expectedResults = []
    for lines in testLines:
        expectedResults.append(lines.strip())
    assert str(excelLinearConverter.excelToLinear("Monday")) == str(expectedResults[0])
    assert str(excelLinearConverter.excelToLinear("Tuesday")) == str(expectedResults[1])
    assert str(excelLinearConverter.excelToLinear("Wednesday")) == str(expectedResults[2])
    assert str(excelLinearConverter.excelToLinear("Thursday")) == str(expectedResults[3])
    assert str(excelLinearConverter.excelToLinear("Friday")) == str(expectedResults[4])
    assert str(excelLinearConverter.excelToLinear("Saturday")) == str(expectedResults[5])
    assert str(excelLinearConverter.excelToLinear("Sunday")) == str(expectedResults[6])
    assert str(excelLinearConverter.excelToLinear("Alt A")) == str(expectedResults[7])
    assert str(excelLinearConverter.excelToLinear("Alt B")) == str(expectedResults[8])
    assert str(excelLinearConverter.excelToLinear("Alt C")) == str(expectedResults[9])


def activityTypeTest():
    assert excelLinearConverter.activityType('FF0070C0') == "Studying"
    


if __name__ == "__main__":
    converterTest()