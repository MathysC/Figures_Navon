#include "gridcanvas.h"
using namespace std;


vector<int> bitVector (25,0);
gridcanvas::gridcanvas(QWidget *parent, int numberOfCells, int canvas_width) : QWidget()
{
//    cout << "vector before replacement" << endl;
    vector<int>::iterator pos;
    for(pos = bitVector.begin(); pos!=bitVector.end(); ++pos)
//       cout << *pos;
//    cout << endl;
    this->sizeOfCell = canvas_width/numberOfCells;
    this->canvas_width = 480;
    this->numberOfCells = 5;
    graphicsview = new QGraphicsView(this);
    scene = new QGraphicsScene(0,0,canvas_width,canvas_width);
    pixmapItem = new QGraphicsPixmapItem();
    drawGrid();
    scene->addItem(pixmapItem);
    graphicsview->setScene(scene);

}


void gridcanvas::drawGrid()
{
    QPixmap map(scene->width(),scene->width());
    map.fill();
    QPainter painter;
    painter.begin(&map);
    painter.setPen(*(new QColor(0,0,0,255)));
    for(int xstep = 0; xstep < this->canvas_width; xstep+=this->sizeOfCell){
        for(int ystep=0; ystep < this->canvas_width; ystep+=this->sizeOfCell){
            painter.drawRect(xstep,ystep,this->sizeOfCell,this->sizeOfCell);
        }
    }
    pixmapItem->setPixmap(map);
    scene->addPixmap(map);

}

void gridcanvas::paintOnGrid(QMouseEvent *event)
{
    int squareXIndex = event->x()/sizeOfCell;
    int squareYIndex = event->y()/sizeOfCell;
//    Fills the bitVector with a 1 where there is a squarepainted.
    int squareIndex= squareXIndex + squareYIndex * this->numberOfCells;
    fillVector(squareIndex);
    int squareX = squareXIndex*sizeOfCell;
    int squareY = squareYIndex*sizeOfCell;
    paintedSquare = new QGraphicsRectItem(squareX, squareY,sizeOfCell, sizeOfCell);
    paintedSquare->setBrush(Qt::black);
    scene->addItem(paintedSquare);
    update();
}

//Simply generates the bit vector, with a size matching the number of cells on the grid.
void gridcanvas::generateVector()
{
    bitVector.resize(this->numberOfCells*numberOfCells, 0);
//    cout << "bitVector size = " << bitVector.size() << endl;

//    resets all the bit to 0 for when the grid changes, since all the squares are erased.
    replace(bitVector.begin(),bitVector.end(),1,0);

}

void gridcanvas::fillVector(int index)
{
    vector<int>::iterator pos;
    bitVector[index] = 1;


}

std::vector<int> gridcanvas::getVector()
{
    return bitVector;
}

void gridcanvas::setWidthValue(int value)
{
    this->canvas_width = 480 + value*48;
    this->scene->setSceneRect(0,0,canvas_width,canvas_width);
    this->graphicsview->adjustSize();
    generateVector();
}

void gridcanvas::setNumberOfCells(int value)
{
    this->numberOfCells = value;
    generateVector();
    update();
}

void gridcanvas::setSizeOfCells()
{
    squares.clear();

    this->sizeOfCell = this->canvas_width/this->numberOfCells;
    drawGrid();
    update();
}

int gridcanvas::getCanvasWidth()
{
    return canvas_width;
}

int gridcanvas::getNumberOfCells()
{
    return this->numberOfCells;
}

void gridcanvas::update()
{
    this->pixmapItem->update();
    window()->update();
    this->scene->update();
    this->graphicsview->update();

}

void gridcanvas::mousePressEvent(QMouseEvent *event)
{
    if(event->button() == Qt::LeftButton)
    {
        paintOnGrid(event);
        scribbling = true;
    }
}

void gridcanvas::mouseMoveEvent(QMouseEvent *event)
{
    if(event->button() == Qt::LeftButton && scribbling)
    {
        paintOnGrid(event);
    }

}

void gridcanvas::mouseReleaseEvent(QMouseEvent *event)
{
    if (event->button() == Qt::LeftButton && scribbling) {
        scribbling = false;
    }
}


gridcanvas::~gridcanvas()
{
    free(this);
}
