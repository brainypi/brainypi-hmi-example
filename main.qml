import QtQuick 2.12
import QtQuick.Controls 2.12
import QtCharts 2.3
import QtDataVisualization 1.15
import QtQuick.Layouts 1.12

ApplicationWindow {
    visible: true
    width: 800
    height: 480
    title: "HMI"
    color: "#F2F2F2"
    
   GridLayout {
        columns: 2
        rows: 2
        Layout.fillHeight: true
        Layout.fillWidth: true
    	anchors.top: parent.top
    	anchors.bottom: parent.bottom
    	anchors.left: parent.left
    	anchors.right: parent.right

        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            border.width: 1
            // Part 1: Vertical sliders for temperature and pressure
            RowLayout {
                spacing: 50
                anchors.horizontalCenter: parent.horizontalCenter
                Slider {
                    id: temperatureSlider
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.horizontalCenterOffset: -50
                    value: 20
                    from: 0
                    to: 100
                    orientation: Qt.Vertical
                    stepSize: 1
                    snapMode: Slider.SnapAlways
                }
                Label {
                    text: "Temperature"
                    font.pointSize: 16
                    anchors.horizontalCenter: temperatureSlider.horizontalCenter
                    anchors.top: temperatureSlider.bottom
                    anchors.topMargin: 10
                }
                Slider {
                    id: pressureSlider
                    anchors.left: temperatureSlider.right
                    anchors.leftMargin: 70
                    value: 50
                    from: 0
                    to: 100
                    orientation: Qt.Vertical
                    stepSize: 1
                    snapMode: Slider.SnapAlways
                }
                Label {
                    text: "Pressure"
                    font.pointSize: 16
                    anchors.horizontalCenter: pressureSlider.horizontalCenter
                    anchors.top: pressureSlider.bottom
                    anchors.topMargin: 10
                }
            }
        }
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            border.width: 1

            // Part 2: Text components to display data
            RowLayout {
                spacing: 20
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.leftMargin: 10
                Layout.rightMargin: 10
                Text {
                    id: temperatureValue
                    anchors.horizontalCenter: parent.horizontalCenter - 10
                    text: "Temperature: " + temperatureSlider.value.toFixed(1) + " °C"
                    font.pixelSize: 20
                }
                Text {
                    id: pressureValue
                    anchors.horizontalCenter: parent.horizontalCenter + 100
                    text: "Pressure: " + (pressureSlider.value + 100).toFixed(1) + " kPa"
                    font.pixelSize: 20
                }
            }
        }
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            border.width: 1
            ChartView {
                id: chart1
                anchors.fill: parent
                theme: ChartView.ChartThemeBrownSand
                antialiasing: true
                LineSeries {
                    id: line1
                    axisX: ValueAxis {
                        min: 0
                        max: 100
                        tickCount: 1
                    }
                    axisY: ValueAxis {
                        min: 0
                        max: 100
                        tickCount: 1
                    }
                    name: "Pump Temperature"
                }
            }

        }
        Rectangle {
            Layout.fillHeight: true
            Layout.fillWidth: true
            border.width: 1
            ChartView {
                id: chart2
                theme: ChartView.ChartThemeBlueCerulean
                anchors.fill: parent
                antialiasing: true

                LineSeries {
                    id: line2
                    axisX: ValueAxis {
                        min: 0
                        max: 100
                        tickCount: 1
                    }
                    axisY: ValueAxis {
                        min: 0
                        max: 100
                        tickCount: 1
                    }
                    name: "Pump Pressure"
                }
            }
        }
        Timer {
           interval: 500
           repeat: true
           running: true

           onTriggered: {
               // Update chart values
               var xValue1 = line1.count;
               var yValue1 = Math.floor(Math.random()*100);
               line1.append(xValue1, yValue1);
               // Update chart values
               var xValue2 = line2.count;
               var yValue2 = Math.floor(Math.random()*100);
               line2.append(xValue2, yValue2);
           }
       }
    }
}    

