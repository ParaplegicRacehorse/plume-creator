/***************************************************************************
*   Copyright (C) 2021 by Cyril Jacquet                                 *
*   cyril.jacquet@skribisto.eu                                        *
*                                                                         *
*  Filename: plugin.cpp
*                                                  *
*  This file is part of Skribisto.                                    *
*                                                                         *
*  Skribisto is free software: you can redistribute it and/or modify  *
*  it under the terms of the GNU General Public License as published by   *
*  the Free Software Foundation, either version 3 of the License, or      *
*  (at your option) any later version.                                    *
*                                                                         *
*  Skribisto is distributed in the hope that it will be useful,       *
*  but WITHOUT ANY WARRANTY; without even the implied warranty of         *
*  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          *
*  GNU General Public License for more details.                           *
*                                                                         *
*  You should have received a copy of the GNU General Public License      *
*  along with Skribisto.  If not, see <http://www.gnu.org/licenses/>. *
***************************************************************************/
#include "plugin.h"
#include "skrdata.h"
#include "skrplumecreatorimporter.h"
#include <QQmlApplicationEngine>

Plugin::Plugin(QObject *parent) : QObject(parent)
{
    qmlRegisterType<SKRPlumeCreatorImporter>("eu.skribisto.plumecreatorimporter",
                                             1,
                                             0,
                                             "SKRPlumeCreatorImporter");
}

// ---------------------------------------------------

Plugin::~Plugin()
{}


// ---------------------------------------------------
