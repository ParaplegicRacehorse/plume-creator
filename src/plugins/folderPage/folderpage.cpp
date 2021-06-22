/***************************************************************************
*   Copyright (C) 2021 by Cyril Jacquet                                 *
*   cyril.jacquet@skribisto.eu                                        *
*                                                                         *
*  Filename: folderpage.cpp                                                   *
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
#include "folderpage.h"
#include "skrdata.h"

FolderPage::FolderPage(QObject *parent) : QObject(parent)
{


}

// ---------------------------------------------------

FolderPage::~FolderPage()
{}

// ---------------------------------------------------

SKRResult FolderPage::finaliseAfterCreationOfTreeItem(int projectId, int treeItemId)
{
    SKRResult result(this);

    return result;
}

// ---------------------------------------------------

void FolderPage::updateCharAndWordCount(int projectId, int treeItemId, bool sameThread)
{
}

// ---------------------------------------------------
QTextDocumentFragment FolderPage::generateExporterTextFragment(int                projectId,
                                                             int                treeItemId,
                                                             const QVariantMap& exportProperties,
                                                             SKRResult        & result) const
{
    QTextDocument *document = nullptr;


    return QTextDocumentFragment(document);
}
