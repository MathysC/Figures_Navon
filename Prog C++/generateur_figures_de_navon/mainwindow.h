#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsView>
#include <QGraphicsScene>
#include <QMouseEvent>
#include <QSlider>
#include <QLayout>
#include <QFormLayout>
#include <QSpinBox>
#include <QLabel>
#include <QLineEdit>
#include <QPushButton>
#include <QFile>
#include <QTextStream>
#include <QFileDialog>

#include "gridcanvas.h"
#include "navonfigure.h"

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    QLabel *sizeLabel;
    QLabel *nbCellsLabel;
    string txtFilePath;
    void saveChanges();


    ~MainWindow();

signals:
    void setValue(int value);
    void on_widthSliderPressed();

private slots:
    void updateWidthLabel();
    void updateCellsLabel();
    void chooseTxtInputFile();
    void generateImage();




private:
    Ui::MainWindow *ui;
    gridcanvas *grid;
    NavonFigure* navon;
    QLabel* pathChoosenLabel;

};
#endif // MAINWINDOW_H
