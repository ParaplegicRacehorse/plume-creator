/***************************************************************************
 *   Copyright (C) 2019 by Cyril Jacquet                                 *
 *   cyril.jacquet@skribisto.eu                                        *
 *                                                                         *
 *  Filename: plmpropertiesproxymodel.h                                                   *
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
#ifndef SKRPROPERTIESPROXYMODEL_H
#define SKRPROPERTIESPROXYMODEL_H

#include <QObject>
#include "./skribisto_data_global.h"

class EXPORT SKRPropertiesProxyModel : public QObject
{
    Q_OBJECT
public:
    explicit SKRPropertiesProxyModel(QObject *parent = nullptr);

signals:

public slots:
};

#endif // SKRPROPERTIESPROXYMODEL_H
