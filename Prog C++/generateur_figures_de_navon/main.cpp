#include "mainwindow.h"
#include "navonfigure.h"
#include <QApplication>
#include <iostream>
#include <QDir>
using namespace std;

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;

    w.show();


    return a.exec();
}
