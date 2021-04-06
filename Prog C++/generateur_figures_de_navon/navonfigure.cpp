#include "navonfigure.h"
#include "math.h"


using namespace std;


NavonFigure::NavonFigure(char character, int fontSize, int spanning)
{
    this->shape=shape;
    this->character=character;
    this->fontSize = fontSize;
    this->spanning = spanning;
}

NavonFigure::~NavonFigure()
{
    free(this);
}

void NavonFigure::drawFigureFromFile(string filepath, QString imagePath)
{
    fstream figureFile;
    vector<int> globalShape;
    string line;
    bool figureStored = false;
    int figureNum=0;
    int arrIndex=0;
    figureFile.open(filepath,ios::in);
    if(figureFile.is_open()){
        while(!figureFile.eof()){
            getline(figureFile,line, '\n');
            for(int i =0; i<line.size(); i++){
                char c[] = {line[i]};
                if(c[0] == '1' || c[0] == '0'){
                    globalShape.push_back(stoi(c));
                    arrIndex++;
}
//given that each shape arrays end with a ] in the txt file we reset the arrIndex to 0
//to rewrite globalShape with the next shape.
                if(c[0]==']')
                {
                    figureStored = true;
                }
            }
//arrIndex represents the 20 indexes that serve to represent a shape in a array.
//this will have to change as we are expecting representation to be of various size.
//Until then this means a shape has been fully stored in the array.
//It then prints the shape and resets the arrIndex to move on to the next shape.
            if(figureStored)
            {
                arrIndex=0;
                int i;
                QChar local_char = this->character;
                QImage image(960, 960, QImage::Format_RGB32);
                image.fill(QColor(250,250,250));
                QPainter painter(&image);
                painter.setFont(QFont("Times",fontSize));
                QPoint topLeft(0,0);
                QPoint bottomRight(fontSize, fontSize);
                QRect rect(topLeft, bottomRight);
                for(i=0; i<globalShape.size(); i++){
                    if(i%int(sqrt(globalShape.size())) == 0)
                    {
                        topLeft.setX(0); topLeft.setY(topLeft.y()+fontSize+spanning);
                        bottomRight.setX(fontSize+spanning); bottomRight.setY(bottomRight.y()+fontSize+spanning);
                    }
                    if(globalShape[i] == 1)
                    {
                        rect.setTopLeft(topLeft); rect.setBottomRight(bottomRight);
                        painter.drawText(rect, Qt::AlignCenter, local_char);
                    }
                    topLeft.setX(topLeft.x()+fontSize+spanning);
                    bottomRight.setX(bottomRight.x()+fontSize+spanning);
                }
                bool isSaved = image.save(imagePath, "PNG", 100);
            }
        }
    }
    else{
    }
    figureFile.close();
}

void NavonFigure::setFontSize(int i)
{
    this->fontSize = i;
}

void NavonFigure::setSpanning(int i)
{
    this->spanning = i;
}

void NavonFigure::setCharacter(QString text){
    QByteArray ba = text.toLocal8Bit();
    const char *character_array = ba.data();
    char character = character_array[0];
    this->character = character;
}



