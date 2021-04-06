#ifndef GRIDCANVAS_H
#define GRIDCANVAS_H

#include <QMainWindow>
#include <QGraphicsItem>
#include <QGraphicsView>
#include <QWidget>
#include <QMouseEvent>
#include <QSlider>
#include <QGraphicsRectItem>
#include <iostream>
#include <list>
#include "ui_mainwindow.h"


class gridcanvas: public QWidget
{
public:
    int numberOfCells,canvas_width;
    int sizeOfCell;
//    std::vector<int> bitVector;
    gridcanvas(QWidget *parent = nullptr, int numberOfCells = 5, int canvas_width = 480);
    ~gridcanvas();
    void update();
    void generateVector();
    void fillVector(int index);
    std::vector<int> getVector();

signals:

public slots:
    void setWidthValue(int value);
    void setNumberOfCells(int value);
    void setSizeOfCells();
    void paintOnGrid(QMouseEvent *event);
    int getNumberOfCells();
    int getCanvasWidth();

protected:
    void mousePressEvent(QMouseEvent *event) override;
    void mouseMoveEvent(QMouseEvent *event) override;
    void mouseReleaseEvent(QMouseEvent *event) override;

private:

    QGraphicsScene *scene;
    QGraphicsView *graphicsview;
    QGraphicsPixmapItem *pixmapItem;
    QPixmap map;
    Ui::MainWindow *ui;
    QGraphicsRectItem *paintedSquare;
    QGraphicsItemGroup *squareGroup;
    std::list<QGraphicsRectItem*> squares;
    bool scribbling;
    void drawGrid();


};

#endif // GRIDCANVAS_H
