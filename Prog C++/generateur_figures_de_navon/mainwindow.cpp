#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    this->setWindowTitle("Navon Generator");
    grid = new gridcanvas();
    navon = new NavonFigure();

//    slider to control the size of the canvas
    sizeLabel = new QLabel();
    QString size = "Zoom";
    sizeLabel->setText(size);
    nbCellsLabel = new QLabel();
    QString nbCells = "number of cells = " + QString::number(grid->getNumberOfCells());
    nbCellsLabel->setText(nbCells);
//    QString size = "cellSize = " + QString::number(grid->getCanvasWidth());
//    sizeLabel->setText(size);

    QSlider* widthSlider = new QSlider(Qt::Horizontal, this);
    widthSlider->setMinimum(0);
    widthSlider->setMaximum(9);

//    slider to control the number of cells (or squares) of the grid
    QSlider* cellsSlider = new QSlider(Qt::Horizontal, this);
    cellsSlider->setMinimum(5);
    cellsSlider->setMaximum(60);

    QLineEdit *savePath = new QLineEdit;
    savePath->setText("name of the shape");
    QHBoxLayout* mainWidgets = new QHBoxLayout;
    mainWidgets->addWidget(grid);
    mainWidgets->addWidget(savePath);


    QGridLayout *sliderGrid = new QGridLayout;
    sliderGrid->addWidget(sizeLabel,0,0);
    sliderGrid->addWidget(nbCellsLabel,1,0);
    sliderGrid->addWidget(widthSlider,0,1);
    sliderGrid->addWidget(cellsSlider,1,1);
    QHBoxLayout* sizeHBox = new QHBoxLayout;
    sizeHBox->addWidget(sizeLabel);
    sizeHBox->addWidget(widthSlider);


    QPushButton *validationButton = new QPushButton;
    validationButton->setText("Create .txt file");
    QHBoxLayout* formHbox = new QHBoxLayout;
    formHbox->addWidget(validationButton);

    QVBoxLayout* leftLayout = new QVBoxLayout;
    leftLayout->addWidget(grid);
    leftLayout->addLayout(sliderGrid);
    leftLayout->addLayout(formHbox);

    QPushButton* choosePathButton = new QPushButton;
    choosePathButton->setText("Choose File");

    pathChoosenLabel = new QLabel;
    pathChoosenLabel->setText("txt file loaded : ");

    pathChoosenLabel->setSizePolicy(QSizePolicy::Ignored, QSizePolicy::Fixed);
    QPushButton* generateImageButton = new QPushButton;
    generateImageButton->setText("Generate Image");

    QSpinBox* fontSizeSpin = new QSpinBox;
    fontSizeSpin->setMinimum(9);
    fontSizeSpin->setMaximum(30);
    QSpinBox* spacingSpin = new QSpinBox;
    spacingSpin->setMinimum(-10);
    spacingSpin->setMaximum(10);
    QLineEdit* charEdit = new QLineEdit;
    QFormLayout* formLayout = new QFormLayout;
    formLayout->addRow(tr("font size"), fontSizeSpin);
    formLayout->addRow(tr("spacing"), spacingSpin);
    formLayout->addRow(tr("local character"), charEdit);

    QVBoxLayout* rightLayout = new QVBoxLayout;
    rightLayout->addWidget(pathChoosenLabel);
    rightLayout->addWidget(choosePathButton);
    rightLayout->addWidget(generateImageButton);
    rightLayout->addItem(formLayout);

    QHBoxLayout* mainLayout = new QHBoxLayout;
    mainLayout->addItem(leftLayout);
    mainLayout->addItem(rightLayout);

    ui->centralwidget->setLayout(mainLayout);

    //signals that interact with the sliders, and which change the properties of the canvas
    connect(widthSlider, &QSlider::valueChanged, grid, &gridcanvas::setWidthValue);
    connect(widthSlider, &QSlider::valueChanged, grid, &gridcanvas::setSizeOfCells);
    connect(cellsSlider, &QSlider::valueChanged, this, &MainWindow::updateCellsLabel);
    connect(cellsSlider, &QSlider::valueChanged, grid, &gridcanvas::setNumberOfCells);
    connect(cellsSlider, &QSlider::valueChanged, grid, &gridcanvas::setSizeOfCells);
    connect(validationButton, &QPushButton::clicked, this, &MainWindow::saveChanges);
    connect(fontSizeSpin, QOverload<int>::of(&QSpinBox::valueChanged), navon, &NavonFigure::setFontSize);
    connect(spacingSpin, QOverload<int>::of(&QSpinBox::valueChanged), navon, &NavonFigure::setSpanning);


    connect(charEdit, &QLineEdit::textChanged, navon, &NavonFigure::setCharacter);
    connect(choosePathButton, &QPushButton::clicked, this, &MainWindow::chooseTxtInputFile);
    connect(generateImageButton, &QPushButton::clicked, this, &MainWindow::generateImage);

}

void MainWindow::updateWidthLabel()
{
    QString size = "screen width = " + QString::number(grid->getCanvasWidth());
    sizeLabel->setText(size);
//    cout << "size of cells = "<< grid->getCanvasWidth()<< endl;

}

void MainWindow::updateCellsLabel()
{
    QString nbCells = "number of cells = " + QString::number(grid->getNumberOfCells());
    nbCellsLabel->setText(nbCells);
//    cout << "size of cells = "<< grid->getCanvasWidth()<< endl;

}

void MainWindow::saveChanges()
{
    QString fileName = QFileDialog::getSaveFileName(this, tr("Save File"),
                           QDir::homePath(),
                           tr("text (*.txt)"));
//    cout << "fileName is : " <<qPrintable(fileName ) << endl;
    QFile file(fileName);
    if (!file.open(QIODevice::WriteOnly | QIODevice::Text | QIODevice::Append))
        return;
//    file.seek(file.size());
    QTextStream out(&file);

    out << "shape = [" << endl;

    std::vector<int> vector = grid->getVector();
    int i = 0;
    std::vector<int>::iterator pos;
    for(pos = vector.begin(); pos!=vector.end(); ++pos)
    {
       if(i%grid->getNumberOfCells()==0)
           out << endl;
       out << *pos <<",";
       i++;
    }
    out << endl << "]" << endl;
}

void MainWindow::chooseTxtInputFile()
{
    QString file = QFileDialog::getOpenFileName(this,
    tr("Load txt file"), QDir::homePath(), tr("Text Files (*.txt)"));
    this->txtFilePath = file.toUtf8().constData();
    pathChoosenLabel->setText("txt file loaded : " + QString::fromUtf8(txtFilePath.c_str()));
    pathChoosenLabel->update();


}

void MainWindow::generateImage()
{
    QString file = QFileDialog::getSaveFileName(this,
    tr("Save Image"), QDir::homePath(), tr("Image Files (*.png *.jpg *.bmp)"));
    navon->drawFigureFromFile(txtFilePath, file);

}

MainWindow::~MainWindow()
{
    delete ui;
}


