/***************************************************************************
*   Copyright (C) 2016 by Cyril Jacquet                                 *
*   cyril.jacquet@skribisto.eu                                        *
*                                                                         *
*  Filename: plmsheethub.h                                                   *
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
#ifndef PLMSHEETHUB_H
#define PLMSHEETHUB_H

#include <QObject>
#include "plmpaperhub.h"
#include "skribisto_data_global.h"

class EXPORT PLMSheetHub : public PLMPaperHub {
    Q_OBJECT

public:

    PLMSheetHub(QObject *parent);


    QHash<QString, QVariant>getSheetData(int projectId,
                                         int sheetId) const;

    Q_INVOKABLE SKRResult    setTitle(int            projectId,
                                     int            paperId,
                                     const QString& newTitle);

    Q_INVOKABLE SKRResult       addPaperAbove(int projectId,
                                             int targetId);
    Q_INVOKABLE SKRResult       addPaperBelow(int projectId,
                                             int targetId);
    Q_INVOKABLE SKRResult       addChildPaper(int projectId,
                                             int targetId);
    Q_INVOKABLE SKRResult       setTrashedWithChildren(int  projectId,
                                                      int  paperId,
                                                      bool newTrashedState);
    Q_INVOKABLE SKRResult       untrashOnlyOnePaper(int projectId,
                                                   int paperId);

    SKRResult                   removePaper(int projectId,
                                           int targetId);

    Q_INVOKABLE  QList<QString>getAttributes(int projectId,
                                             int paperId) override;
    Q_INVOKABLE  bool          hasAttribute(int            projectId,
                                            int            paperId,
                                            const QString& attribute) override;
    Q_INVOKABLE  SKRResult      addAttribute(int            projectId,
                                            int            paperId,
                                            const QString& attribute) override;
    Q_INVOKABLE SKRResult       removeAttribute(int            projectId,
                                               int            paperId,
                                               const QString& attribute) override;
};

#endif // PLMSHEETHUB_H
