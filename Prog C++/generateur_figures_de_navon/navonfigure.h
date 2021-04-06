#ifndef NAVONFIGURE_H
#define NAVONFIGURE_H
#include <string>
#include <fstream>
#include <iostream>
#include <QPainter>
#include <QRect>
#include <QPoint>
#include <QTranslator>
#include <QStringBuilder>
#include "gridcanvas.h"
using namespace std;

class NavonFigure : public QWidget
{
    public:
        string shape;
        char character;
        int fontSize;
        int spanning;

        NavonFigure(char character = 'a', int fontSize = 12, int spanning = 0);
        ~NavonFigure();
        void setShape(string shape);
        void drawFigureFromFile(string filepath, QString imagePath);

    public slots:
        void setFontSize(int i);
        void setCharacter(QString text);
        void setSpanning(int i);
    private:


};



#endif // NAVONFIGURE_H
