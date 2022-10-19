/***************************************************************************
*   Copyright (C) 2021 by Cyril Jacquet                                 *
*   cyril.jacquet@skribisto.eu                                        *
*                                                                         *
*  Filename: skrtreehub.cpp                                                   *
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
#include "skrtreehub.h"
#include "sql/plmsqlqueries.h"
#include "tools.h"
#include "skrdata.h"

#include <QCollator>
#include <QHash>

SKRTreeHub::SKRTreeHub(QObject *parent) : QObject(parent), m_tableName("tbl_tree"), m_last_added_id(-1), m_cutCopy(
                                                                                                             CutCopy())
{
    connect(this,                  &SKRTreeHub::errorSent,        this, &SKRTreeHub::setError, Qt::DirectConnection);

    // reset m_cutCopy
    connect(skrdata->projectHub(), &PLMProjectHub::projectClosed, this, [this](int projectId) {
        if (m_cutCopy.projectId == projectId) {
            m_cutCopy = CutCopy();
        }
    });
}

// ----------------------------------------------------------------------------------------

QHash<int, int>SKRTreeHub::getAllSortOrders(int projectId) const
{
    SKRResult result(this);

    QHash<int, int> hash;
    QHash<int, QVariant> out;
    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.getValueByIds("l_sort_order", out, "", QVariant(), true);
    IFOK(result) {
        hash = HashIntQVariantConverter::convertToIntInt(out);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return hash;
}

// ----------------------------------------------------------------------------------------

QHash<int, int>SKRTreeHub::getAllIndents(int projectId) const
{
    SKRResult result(this);

    QHash<int, int> hash;
    QHash<int, QVariant> out;
    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.getValueByIds("l_indent", out, "", QVariant(), true);
    IFOK(result) {
        hash = HashIntQVariantConverter::convertToIntInt(out);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return hash;
}

// ----------------------------------------------------------------------------------------

///
/// \brief SKRTreeHub::getAllIds
/// \param projectId
/// \return
/// Get sorted ids, trashed ids included
QList<int>SKRTreeHub::getAllIds(int projectId) const
{
    SKRResult result(this);

    QList<int> list;
    QList<int> out;
    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.getSortedIds(out);
    IFOK(result) {
        list = out;
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return list;
}

QList<QVariantMap> SKRTreeHub::saveTree(int projectId) const
{
    SKRResult result(this);

    PLMSqlQueries queries(projectId, m_tableName);
    QStringList fieldNames = queries.getAllFieldTitles();

    QVariantMap allFields;
    QList<QVariantMap> list;

    for(int treeItemId : this->getAllIds(projectId)){

        for(const QString &fieldName : fieldNames) {
            allFields.insert(fieldName, this->get(projectId, treeItemId, fieldName));
        }

        list.append(allFields);
    }

    IFKO(result) {
        emit errorSent(result);
    }

    return list;

}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::restoreTree(int projectId, QList<QVariantMap> allValues)
{
    SKRResult result(this);

    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.injectDirectSql("PRAGMA foreign_keys = 0");
    result = queries.injectDirectSql("DELETE FROM tbl_tree");

    for(const QVariantMap &values : allValues){

        QHash<QString, QVariant> hash;
        QVariantMap::const_iterator i = values.constBegin();
        while (i != values.constEnd()) {
            hash.insert(i.key(), i.value());
            ++i;
        }
        int newId;
        queries.add(hash, newId);

    }
    result = queries.injectDirectSql("PRAGMA foreign_keys = 1");
    this->commit(projectId);

    IFOK(result) {
        emit treeReset(projectId);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;

}

// ----------------------------------------------------------------------------------------

QVariantMap SKRTreeHub::saveId(int projectId, int treeItemId) const
{
    SKRResult result(this);

    PLMSqlQueries queries(projectId, m_tableName);
    QStringList fieldNames = queries.getAllFieldTitles();

    QVariantMap allFields;

    for(const QString &fieldName : fieldNames) {
        allFields.insert(fieldName, this->get(projectId, treeItemId, fieldName));
    }

    IFKO(result) {
        emit errorSent(result);
    }

    return allFields;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::restoreId(int projectId, int treeItemId, const QVariantMap &values)
{
    SKRResult result(this);

    QVariantMap::const_iterator i = values.constBegin();
    while (i != values.constEnd()) {
        result = set(projectId, treeItemId, i.key(), i.value(), false, false);
        ++i;
    }
    this->commit(projectId);


    IFOK(result) {
        // do like if a tree item was added :
        emit treeItemAdded(projectId, treeItemId);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTreeItemId(int projectId, int treeItemId, int newId)
{

    SKRResult result = set(projectId, treeItemId, "l_tree_id", newId);

    IFOK(result) {
        emit treeItemIdChanged(projectId, treeItemId, newId);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTitle(int projectId, int treeItemId, const QString& newTitle)
{
    SKRResult result = set(projectId, treeItemId, "t_title", newTitle);

    IFOK(result) {
        emit titleChanged(projectId, treeItemId, newTitle);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QString SKRTreeHub::getTitle(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "t_title").toString();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setInternalTitle(int projectId, int treeItemId, const QString& internalTitle)
{

    SKRResult result = set(projectId, treeItemId, "t_internal_title", internalTitle);

    IFOK(result) {
        emit internalTitleChanged(projectId, treeItemId, internalTitle);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::removeInternalTitleFromAll(int projectId, const QString& internalTitle)
{
    SKRResult result(this);

    QList<int> idList = this->getAllIds(projectId);

    for (int id : qAsConst(idList)) {
        if (this->getInternalTitle(projectId, id) == internalTitle) {
            result = this->setInternalTitle(projectId, id, "");
        }
    }

    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getIdsWithInternalTitle(int projectId, const QString& internalTitle) const
{
    SKRResult result(this);
    QHash<int, QVariant> out;

    QHash<QString, QVariant> where;

    where.insert("t_internal_title", internalTitle);

    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.getValueByIdsWhere("t_title", out, where);

    return out.keys();
}

// ----------------------------------------------------------------------------------------

QString SKRTreeHub::getInternalTitle(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "t_internal_title").toString();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setIndent(int projectId, int treeItemId, int newIndent)
{
     return this->setIndent(projectId, treeItemId, newIndent, true, true);
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setIndent(int projectId, int treeItemId, int newIndent, bool setCurrentdate, bool commit)
{
    SKRResult result = set(projectId, treeItemId, "l_indent", newIndent, setCurrentdate, commit);

    IFOK(result) {
        emit indentChanged(projectId, treeItemId, newIndent);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getIndent(int projectId, int treeItemId) const
{
    int indent;

    if (treeItemId == -1) // is project item
        indent = -1;
    else {
        indent = get(projectId, treeItemId, "l_indent").toInt();
    }

    return indent;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setSortOrder(int projectId, int treeItemId, int newSortOrder)
{
    return this->setSortOrder(projectId, treeItemId, newSortOrder, true, true);
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setSortOrder(int projectId, int treeItemId, int newSortOrder, bool setCurrentdate, bool commit)
{
    SKRResult result = set(projectId, treeItemId, "l_sort_order", newSortOrder, setCurrentdate, commit);

    IFOK(result) {
        emit sortOrderChanged(projectId, treeItemId, newSortOrder);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getSortOrder(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "l_sort_order").toInt();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setType(int projectId, int treeItemId, const QString& newType)
{
    SKRResult result = set(projectId, treeItemId, "t_type", newType);

    IFOK(result) {
        emit typeChanged(projectId, treeItemId, newType);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QString SKRTreeHub::getType(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "t_type").toString();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setPrimaryContent(int projectId, int treeItemId, const QString& newContent)
{
    return this->setPrimaryContent(projectId, treeItemId, newContent, true, true);
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setPrimaryContent(int            projectId,
                                        int            treeItemId,
                                        const QString& newContent,
                                        bool           setCurrentdate,
                                        bool           commit)
{
    SKRResult result = set(projectId, treeItemId, "m_primary_content", newContent, setCurrentdate, commit);

    IFOK(result) {
        emit primaryContentChanged(projectId, treeItemId, newContent);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QString SKRTreeHub::getPrimaryContent(int projectId, int treeItemId) const
{
    QString content = get(projectId, treeItemId, "m_primary_content").toString();

    return content;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setSecondaryContent(int projectId, int treeItemId, const QString& newContent)
{
    return this->setSecondaryContent(projectId, treeItemId, newContent, true, true);
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setSecondaryContent(int            projectId,
                                          int            treeItemId,
                                          const QString& newContent,
                                          bool           setCurrentdate,
                                          bool           commit)
{
    SKRResult result = set(projectId, treeItemId, "m_secondary_content", newContent, setCurrentdate, commit);

    IFOK(result) {
        emit secondaryContentChanged(projectId, treeItemId, newContent);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QString SKRTreeHub::getSecondaryContent(int projectId, int treeItemId) const
{
    QString content = get(projectId, treeItemId, "m_secondary_content").toString();

    return content;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTrashedWithChildren(int projectId, int treeItemId, bool newTrashedState)
{
    SKRResult result(this);

    QList<int> childrenIdList = this->getAllChildren(projectId, treeItemId);


    // children deletion (or recovery)
    for (int& _id : childrenIdList) {
        IFOKDO(result, set(projectId, _id, "b_trashed", newTrashedState));

        // set date but those already deleted
        if (newTrashedState && this->getTrashedDate(projectId, _id).isNull()) {
            result = this->setTrashedDateToNow(projectId, _id);
            emit trashedChanged(projectId, _id, newTrashedState);
        }

        // restore
        else if (!newTrashedState) {
            result = this->setTrashedDateToNull(projectId, _id);
            emit trashedChanged(projectId, _id, newTrashedState);
        }

        // else ignore those already trashed
    }


    // do parent :
    IFOK(result) {
        result = set(projectId, treeItemId, "b_trashed", newTrashedState);

        // set date but those already deleted
        if (newTrashedState && this->getTrashedDate(projectId, treeItemId).isNull()) {
            result = this->setTrashedDateToNow(projectId, treeItemId);
        }

        // restore
        else if (!newTrashedState) {
            result = this->setTrashedDateToNull(projectId, treeItemId);
        }
    }
    IFOK(result) {
        emit trashedChanged(projectId, treeItemId, newTrashedState);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::untrashOnlyOneTreeItem(int projectId, int treeItemId)
{
    SKRResult result = set(projectId, treeItemId, "b_trashed", false);

    IFOKDO(result, this->setTrashedDateToNull(projectId, treeItemId));

    IFOK(result) {
        emit trashedChanged(projectId, treeItemId, false);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

bool SKRTreeHub::getTrashed(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "b_trashed").toBool();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setCreationDate(int projectId, int treeItemId, const QDateTime& newDate)
{
    SKRResult result = set(projectId, treeItemId, "dt_created", newDate);

    IFOK(result) {
        emit creationDateChanged(projectId, treeItemId, newDate);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QDateTime SKRTreeHub::getCreationDate(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "dt_created").toDateTime();
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setUpdateDate(int projectId, int treeItemId, const QDateTime& newDate)
{
    SKRResult result = set(projectId, treeItemId, "dt_updated", newDate);

    IFOK(result) {
        emit updateDateChanged(projectId, treeItemId, newDate);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QDateTime SKRTreeHub::getUpdateDate(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "dt_updated").toDateTime();
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::row(int projectId, int treeItemId) const
{
    int sortOrder = this->getSortOrder(projectId, treeItemId);
    int parentId = this->getParentId(projectId, treeItemId);
    int parentSortOrder = this->getSortOrder(projectId, parentId);

    return (sortOrder - parentSortOrder) / 1000 - 1;

}

// ----------------------------------------------------------------------------------------

bool SKRTreeHub::hasChildren(int projectId, int treeItemId, bool trashedAreIncluded, bool notTrashedAreIncluded) const
{
    SKRResult result(this);
    PLMSqlQueries queries(projectId, m_tableName);

    // if last of id list:
    QList<int> idList;

    IFOKDO(result, queries.getSortedIds(idList));

    if (idList.isEmpty()) { // project item with nothing else
        return false;
    }

    if (treeItemId == idList.last()) {
        return false;
    }

    int indent = getIndent(projectId, treeItemId);

    int possibleFirstChildId;

    if (treeItemId == -1) {                  // project item
        possibleFirstChildId = idList.at(0); // first real treeItem in table
    }
    else {
        possibleFirstChildId = idList.at(idList.indexOf(treeItemId) + 1);
    }


    int possibleFirstChildIndent = getIndent(projectId, possibleFirstChildId);

    // verify indent of child
    if (indent == possibleFirstChildIndent - 1) {
        // verify if at least one child is not trashed
        bool haveOneNotTrashedChild = false;
        bool haveOneTrashedChild    = false;
        int  firstChildIndex        = idList.indexOf(possibleFirstChildId);

        for (int i = firstChildIndex; i < idList.count(); i++) {
            int childId = idList.at(i);
            int indent  = getIndent(projectId, childId);

            if (indent < possibleFirstChildIndent) {
                break;
            }

            if (indent == possibleFirstChildIndent) {
                if (getTrashed(projectId, childId) == false) {
                    haveOneNotTrashedChild = true;
                }
                else {
                    haveOneTrashedChild = true;
                }
            }
        }

        if (haveOneTrashedChild && trashedAreIncluded) {
            return true;
        }

        if (haveOneNotTrashedChild && notTrashedAreIncluded) {
            return true;
        }
        return false;
    }

    IFKO(result) {
        emit errorSent(result);
    }

    return false;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getTopTreeItemId(int projectId) const
{
    int value       = -2;
    QList<int> list = this->getAllIds(projectId);

    for (int id : qAsConst(list)) {
        if (!this->getTrashed(projectId, id)) {
            value = id;
            break;
        }
    }


    return value;
}

// ----------------------------------------------------------------------------------------

QList<int> SKRTreeHub::filterOutChildren(int projectId, QList<int> treeItemIds) const
{
    QList<int> finalList;

    QSet<int> childrenSet;

    for(int id : treeItemIds){
        for(int child : this->getAllChildren(projectId, id)){
            childrenSet.insert(child);
        }
    }
    for(int id : treeItemIds){
        if(!childrenSet.contains(id)){
            finalList.append(id);
        }
    }
    return finalList;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::getError()
{
    return m_error;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::set(int             projectId,
                          int             treeItemId,
                          const QString & fieldName,
                          const QVariant& value,
                          bool            setCurrentDateBool,
                          bool            commit)
{
    SKRResult result(this);
    PLMSqlQueries queries(projectId, m_tableName);

    queries.beginTransaction();
    result = queries.set(treeItemId, fieldName, value);

    if (setCurrentDateBool) {
        IFOKDO(result, queries.setCurrentDate(treeItemId, "dt_updated"));
    }

    IFKO(result) {
        queries.rollback();
    }
    IFOK(result) {
        if (commit) {
            queries.commit();
        }
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

QVariant SKRTreeHub::get(int projectId, int treeItemId, const QString& fieldName) const
{
    SKRResult result(this);
    QVariant  var;
    QVariant  value;
    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.get(treeItemId, fieldName, var);
    IFOK(result) {
        value = var;
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return value;
}

// ----------------------------------------------------------------------------------------

void SKRTreeHub::commit(int projectId)
{
    PLMSqlQueries queries(projectId, m_tableName);
    queries.commit();

}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getLastAddedId()
{
    return m_last_added_id;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::addTreeItem(const QHash<QString, QVariant>& values, int projectId, bool renumber)
{
    PLMSqlQueries queries(projectId, m_tableName);

    queries.beginTransaction();
    int newId        = -1;
    SKRResult result = queries.add(values, newId);

    if(renumber){
        IFOKDO(result, queries.renumberSortOrder());
    }
    IFKO(result) {
        queries.rollback();
    }
    IFOK(result) {
        queries.commit();
    }
    IFKO(result) {
        emit errorSent(result);
    }
    IFOK(result) {
        m_last_added_id = newId;
        result.addData("treeItemId", newId);
        emit treeItemAdded(projectId, newId);
        emit projectModified(projectId);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::addTreeItemAbove(int projectId, int targetId, const QString& type)
{
    int target_indent = getIndent(projectId, targetId);

    SKRResult result(this);
    int finalSortOrder = this->getValidSortOrderBeforeTree(projectId, targetId);

    // finally add treeItem
    QHash<QString, QVariant> values;

    values.insert("l_sort_order", finalSortOrder);
    values.insert("l_indent",     target_indent);
    values.insert("t_type",       type);
    IFOKDO(result, addTreeItem(values, projectId));
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::addTreeItemBelow(int projectId, int targetId, const QString& type)
{
    int target_indent = getIndent(projectId, targetId);

    SKRResult result(this);
    int finalSortOrder = this->getValidSortOrderAfterTree(projectId, targetId);

    // finally add treeItem
    QHash<QString, QVariant> values;

    values.insert("l_sort_order", finalSortOrder);
    values.insert("l_indent",     target_indent);
    values.insert("t_type",       type);
    IFOKDO(result, addTreeItem(values, projectId));
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::addChildTreeItem(int projectId, int targetId, const QString& type)
{
    SKRResult result(this);
    PLMSqlQueries queries(projectId, m_tableName);


    int target_sort_order = getSortOrder(projectId, targetId);
    int target_indent     = getIndent(projectId, targetId);

    // for invalid parent ("root")
    if (targetId == -2) {
        result = SKRResult(SKRResult::Critical, this, "invalid_root_parent");
        return result;
    }

    // for project item as parent :
    if (targetId == 0) {
        target_indent = 0;

        // get the highest sort order
        QHash<int, QVariant> sortOrderResult;
        result = queries.getValueByIds("l_sort_order",
                                       sortOrderResult,
                                       QString(),
                                       QVariant(),
                                       true);

        target_sort_order = 0;

        for (const QVariant& sortOrder : sortOrderResult.values()) {
            target_sort_order = qMax(sortOrder.toInt(), target_sort_order);
        }
    }

    // find next node with the same indentation
    QHash<int, QVariant> hash;
    QHash<QString, QVariant> where;

    where.insert("l_indent <=",    target_indent);
    where.insert("l_sort_order >", target_sort_order);
    result = queries.getValueByIdsWhere("l_sort_order", hash, where, true);
    int finalSortOrder = 0;

    // if node after
    if (!hash.isEmpty()) {
        QHash<int, QVariant>::const_iterator i = hash.constBegin();
        int lowestSort                         = 0;
        lowestSort = i.value().toInt();

        while (i != hash.constEnd()) {
            int sort = i.value().toInt();

            if (sort < lowestSort) {
                lowestSort = sort;
            }

            ++i;
        }

        finalSortOrder = lowestSort - 1;

        // if tree is empty

        if (finalSortOrder == -1) {
            finalSortOrder = 0;
        }
    }

    // if no node after (bottom of tree)
    else {
        QList<int> idList;
        IFOKDO(result, queries.getSortedIds(idList));

        if (idList.isEmpty()) {
            finalSortOrder = 1000;
        } else {
            int lastId = idList.last();
            QHash<int, QVariant> hash2;
            IFOKDO(result,
                   queries.getValueByIds("l_sort_order", hash2, "id",
                                         QVariant(lastId)));
            finalSortOrder = hash2.begin().value().toInt() + 1;
        }
    }

    // finally add treeItem
    QHash<QString, QVariant> values;

    values.insert("l_sort_order", finalSortOrder);
    values.insert("l_indent",     target_indent + 1);
    values.insert("t_type",       type);
    IFOKDO(result, addTreeItem(values, projectId));
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::removeTreeItem(int projectId, int targetId)
{
    PLMSqlQueries queries(projectId, m_tableName);
    emit treeItemAboutToBeRemoved(projectId, targetId);

    queries.beginTransaction();
    SKRResult result = queries.remove(targetId);

    IFOKDO(result, queries.renumberSortOrder());
    IFOKDO(result, queries.trimTreePropertyTable());
    IFOKDO(result, queries.trimTagRelationshipTable());
    IFOKDO(result, queries.trimTreeRelationshipTable());
    IFKO(result) {
        queries.rollback();
    }
    IFOK(result) {
        queries.commit();
    }
    IFKO(result) {
        emit errorSent(result);
    }
    IFOK(result) {
        emit treeItemRemoved(projectId, targetId);
        emit projectModified(projectId);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::moveTreeItem(int sourceProjectId, int sourceTreeItemId,
                                   int  targetProjectId, int targetTreeItemId, bool after)
{
    SKRResult result(this);

    // TODO: adapt to multiple projects


    QList<int> childrenList = this->getAllChildren(sourceProjectId, sourceTreeItemId);

    PLMSqlQueries queries(sourceProjectId, m_tableName);

    if (targetTreeItemId == 0) { // means end of list, so add to end
        after = true;
        int lastChildrenId = this->getAllIds(targetProjectId).last();
        targetTreeItemId = lastChildrenId;
    }


    int targetSortOrder = this->getSortOrder(targetProjectId, targetTreeItemId);
    int targetIndent = this->getIndent(targetProjectId, targetTreeItemId);
    int sourceIndent = this->getIndent(sourceProjectId, sourceTreeItemId);
    int indentDelta = targetIndent - sourceIndent;


    if (after && this->hasChildren(targetProjectId, targetTreeItemId, true, true)) {
        // find the child at the most down of the target
        int lastChildrenId = this->getAllChildren(targetProjectId, targetTreeItemId).last();
        targetTreeItemId = lastChildrenId;
        targetSortOrder  = this->getSortOrder(targetProjectId, lastChildrenId);
    }

    targetSortOrder = targetSortOrder + (after ? 1 : -999);
    result          = setSortOrder(sourceProjectId, sourceTreeItemId, targetSortOrder, true, false);
    result           = setIndent(sourceProjectId, sourceTreeItemId, sourceIndent + indentDelta);

    for (int childId : qAsConst(childrenList)) {
        targetSortOrder += 1;
        result           = setSortOrder(sourceProjectId, childId, targetSortOrder, true, false);

        int childIndent = this->getIndent(sourceProjectId, childId);
        result           = setIndent(sourceProjectId, childId, childIndent + indentDelta);
    }

    childrenList.prepend(sourceTreeItemId);

    IFOKDO(result, queries.renumberSortOrder())

            IFKO(result) {
        queries.rollback();
        emit errorSent(result);
    }
    IFOK(result) {
        queries.commit();
    }
    IFOK(result) {
        emit treeItemMoved(sourceProjectId, childrenList, targetProjectId, targetTreeItemId);
        emit projectModified(sourceProjectId);

        if (sourceProjectId != targetProjectId) {
            emit projectModified(targetProjectId);
        }
    }

    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::moveTreeItemUp(int projectId, int treeItemId)
{
    SKRResult result(this);

    PLMSqlQueries queries(projectId, m_tableName);

    // get treeItem before this :

    QHash<int, QVariant> sortOrderResult;

    result = queries.getValueByIds("l_sort_order",
                                   sortOrderResult,
                                   QString(),
                                   QVariant(),
                                   true);


    QList<int> idList;

    IFOKDO(result, queries.getSortedIds(idList));

    if (idList.first() == treeItemId) {
        result = SKRResult(SKRResult::Critical, this, "first_in_idList_cant_move_up");
    }
    int targetTreeItemId = -2;

    IFOK(result) {
        // find treeItem before with same indent
        int possibleTargetTreeItemId = -2;

        for (int i = idList.indexOf(treeItemId) - 1; i >= 0; --i) {
            possibleTargetTreeItemId = idList.at(i);

            if (this->getIndent(projectId,
                                possibleTargetTreeItemId) ==
                    this->getIndent(projectId, treeItemId)) {
                targetTreeItemId = possibleTargetTreeItemId;
                break;
            }
        }

        if (possibleTargetTreeItemId == -2) {
            result = SKRResult(SKRResult::Critical, this, "possibleTargetTreeItemId_is_-2");
        }
        IFOK(result) {
            int targetIndent   = this->getIndent(projectId, targetTreeItemId);
            int treeItemIndent = this->getIndent(projectId, treeItemId);

            if (treeItemIndent  != targetIndent) {
                result = SKRResult(SKRResult::Critical, this, "indents_dont_match");
            }
        }
    }
    IFOKDO(result, this->moveTreeItem(projectId, treeItemId, projectId, targetTreeItemId))


            IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::moveTreeItemDown(int projectId, int treeItemId)
{
    SKRResult result(this);

    PLMSqlQueries queries(projectId, m_tableName);

    // get treeItem before this :

    QHash<int, QVariant> sortOrderResult;

    result = queries.getValueByIds("l_sort_order",
                                   sortOrderResult,
                                   QString(),
                                   QVariant(),
                                   true);


    QList<int> idList;

    IFOKDO(result, queries.getSortedIds(idList));

    if (idList.last() == treeItemId) {
        result = SKRResult(SKRResult::Critical, this, "last_in_idList_cant_move_down");
    }
    int targetTreeItemId = -2;

    IFOK(result) {
        // find treeItem after with same indent
        int possibleTargetTreeItemId = -2;

        for (int i = idList.indexOf(treeItemId) + 1; i < idList.count(); ++i) {
            possibleTargetTreeItemId = idList.at(i);

            if (this->getIndent(projectId,
                                possibleTargetTreeItemId) ==
                    this->getIndent(projectId, treeItemId)) {
                targetTreeItemId = possibleTargetTreeItemId;
                break;
            }
        }

        if (possibleTargetTreeItemId == -2) {
            result = SKRResult(SKRResult::Critical, this, "possibleTargetTreeItemId_is_-2");
        }
        IFOK(result) {
            int targetIndent   = this->getIndent(projectId, targetTreeItemId);
            int treeItemIndent = this->getIndent(projectId, treeItemId);

            if (treeItemIndent  != targetIndent) {
                result = SKRResult(SKRResult::Critical, this, "indents_dont_match");
            }
        }
    }
    IFOKDO(result, this->moveTreeItem(projectId, treeItemId, projectId, targetTreeItemId, true))


            IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::moveTreeItemAsChildOf(int  sourceProjectId,
                                            int  sourceTreeItemId,
                                            int  targetProjectId,
                                            int  targetParentId,
                                            bool sendSignal,
                                            int  wantedSortOrder)
{
    SKRResult result(this);


    QList<int> childrenList  = this->getAllChildren(sourceProjectId, sourceTreeItemId);
    int originalSourceIndent =  this->getIndent(sourceProjectId, sourceTreeItemId);

    if (sourceProjectId == targetProjectId) {
        int validSortOrder = getValidSortOrderAfterTree(targetProjectId, targetParentId);


        if (wantedSortOrder == -1) {
            wantedSortOrder = validSortOrder;
        }

        if (wantedSortOrder > validSortOrder) {
            result = SKRResult(SKRResult::Critical, this, "wantedSortOrder_is_outside_scope_of_parent");
        }
        IFOK(result) {
            result = this->setSortOrder(sourceProjectId, sourceTreeItemId, wantedSortOrder);
        }
        IFOK(result) {
            int parentIndent = this->getIndent(targetProjectId, targetParentId);

            result = this->setIndent(sourceProjectId, sourceTreeItemId, parentIndent + 1);

            int i = 0;

            for (int childId : qAsConst(childrenList)) {
                result = this->setSortOrder(sourceProjectId, childId, wantedSortOrder + i);
                i++;

                int orignalSourceChildIndent = this->getIndent(sourceProjectId, childId);
                int delta                    = orignalSourceChildIndent - originalSourceIndent;

                result = this->setIndent(sourceProjectId, childId, parentIndent + 1 + delta);
            }
        }
    }
    else {
        // TODO: move between different projects
    }

    IFKO(result) {
        emit errorSent(result);
    }
    IFOK(result) {
        this->renumberSortOrders(sourceProjectId);
        emit treeItemMoved(sourceProjectId,
                           QList<int>() << sourceTreeItemId << childrenList,
                           targetProjectId,
                           targetParentId);
        emit projectModified(sourceProjectId);

        if (sourceProjectId != targetProjectId) {
            this->renumberSortOrders(targetProjectId);
            emit projectModified(targetProjectId);
        }
    }


    return result;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getParentId(int projectId, int treeItemId) const
{
    int parentId = -2;

    // get indents
    QHash<int, int> indentList = getAllIndents(projectId);
    QList<int> sortedIdList    = getAllIds(projectId);


    // determine direct ancestor

    int indent = indentList.value(treeItemId);

    if (indent == 0) {
        return -1;
    }

    for (int i = sortedIdList.indexOf(treeItemId); i >= 0; i--) {
        int id = sortedIdList.at(i);

        //        if (id == treeItemId) {
        //            continue;
        //        }

        int idIndent = indentList.value(id);

        if (idIndent == indent - 1) {
            parentId = id;
            break;
        }
    }


    return parentId;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::renumberSortOrders(int projectId)
{
    SKRResult result(this);
    PLMSqlQueries queries(projectId, m_tableName);

    result = queries.renumberSortOrder();
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getValidSortOrderBeforeTree(int projectId, int treeItemId) const
{
    int target_sort_order = getSortOrder(projectId, treeItemId);

    int finalSortOrder = target_sort_order - 1;

    return finalSortOrder;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getValidSortOrderAfterTree(int projectId, int treeItemId) const
{
    int target_sort_order = getSortOrder(projectId, treeItemId);
    int target_indent     = getIndent(projectId, treeItemId);

    // find next node with the same indentation
    QHash<int, QVariant> hash;
    QHash<QString, QVariant> where;

    where.insert("l_indent <=",    target_indent);
    where.insert("l_sort_order >", target_sort_order);
    PLMSqlQueries queries(projectId, m_tableName);
    SKRResult     result = queries.getValueByIdsWhere("l_sort_order", hash, where, true);
    int finalSortOrder   = 0;

    // if node after
    if (!hash.isEmpty()) {
        QHash<int, QVariant>::const_iterator i = hash.constBegin();
        int lowestSort                         = 0;
        lowestSort = i.value().toInt();

        while (i != hash.constEnd()) {
            int sort = i.value().toInt();

            if (sort < lowestSort) {
                lowestSort = sort;
            }

            ++i;
        }

        finalSortOrder = lowestSort - 999;

        // if tree is empty
        if (finalSortOrder == -999) {
            finalSortOrder = 1;
        }
    }

    // if no node after (bottom of tree)
    else {
        QList<int> idList;
        IFOKDO(result, queries.getSortedIds(idList));

        if (idList.isEmpty()) {
            result = SKRResult(SKRResult::Critical, this, "idList_is_empty");
        }

        int lastId = idList.last();
        QHash<int, QVariant> hash2;
        IFOKDO(result,
               queries.getValueByIds("l_sort_order", hash2, "id", QVariant(lastId)));
        finalSortOrder = hash2.begin().value().toInt() + 1;
    }

    IFKO(result) {
        emit errorSent(result);
    }

    return finalSortOrder;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::sortAlphabetically(int projectId, int parentTreeItemId)
{
    SKRResult result(this);

    QList<int> directChildren = this->getAllDirectChildren(projectId, parentTreeItemId, true, true);
    QList<int> allChildren    = this->getAllChildren(projectId, parentTreeItemId);
    QList<int> allIds         = this->getAllIds(projectId);

    int parentTreeItemIndexInAllIds = allIds.indexOf(parentTreeItemId);

    QStringList titleList;

    if (directChildren.isEmpty()) {
        return result;
    }

    for (int directChildId : qAsConst(directChildren)) {
        titleList << this->getTitle(projectId, directChildId);
    }

    QCollator collator;
    collator.setCaseSensitivity(Qt::CaseInsensitive);
    collator.setNumericMode(true);
    std::sort(titleList.begin(), titleList.end(), collator);


    QMultiHash<QString, int> allTitlesWithIds;

    for (int directChildId : qAsConst(directChildren)) {
        allTitlesWithIds.insert(this->getTitle(projectId, directChildId), directChildId);
    }

    QList<int> newOrderedDirectChildrenList;

    for (const QString& title : qAsConst(titleList)) {
        QMultiHash<QString, int>::iterator i = allTitlesWithIds.begin();

        while (i != allTitlesWithIds.end()) {
            if (i.key() == title) {
                newOrderedDirectChildrenList.append(i.value());
                i = allTitlesWithIds.erase(i);
            }
            else {
                ++i;
            }
        }
    }


    QList<int> newOrderedIdListPlusChildren;

    bool parentPassed = false;

    for (int id : qAsConst(newOrderedDirectChildrenList)) {
        QList<int> children = skrdata->treeHub()->getAllChildren(projectId, id);

        newOrderedIdListPlusChildren.append(id);
        newOrderedIdListPlusChildren.append(children);
    }


    int newSortOrder = this->getSortOrder(projectId, parentTreeItemId) + 1;

    for (int id : qAsConst(newOrderedIdListPlusChildren)) {
        IFOKDO(result, this->setSortOrder(projectId, id, newSortOrder, true, false));
        newSortOrder += 1;
    }


    IFOKDO(result, this->renumberSortOrders(projectId));
    PLMSqlQueries queries(projectId, m_tableName);

    IFKO(result) {
        queries.rollback();
        emit errorSent(result);
    }
    IFOK(result) {
        queries.commit();

        for (int id : qAsConst(newOrderedDirectChildrenList)) {
            emit sortOrderChanged(projectId, id, this->getSortOrder(projectId, id));
        }
        emit projectModified(projectId);
    }

    return result;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getAllChildren(int projectId, int treeItemId) const
{
    QList<int> childrenList;

    // get indents
    QHash<int, int> indentList = getAllIndents(projectId);
    QList<int> sortedIdList    = getAllIds(projectId);


    // determine children

    int  parentIndent = indentList.value(treeItemId);
    bool parentPassed = false;

    for (int id : qAsConst(sortedIdList)) {
        if (id == treeItemId) {
            parentPassed = true;
            continue;
        }

        if (parentPassed) {
            int idIndent = indentList.value(id);

            if (idIndent > parentIndent) {
                childrenList.append(id);
            }

            if (idIndent <= parentIndent) {
                break;
            }
        }
    }

    return childrenList;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getAllDirectChildren(int  projectId,
                                           int  treeItemId,
                                           bool trashedAreIncluded,
                                           bool notTrashedAreIncluded) const
{
    QList<int> childrenList;

    // get indents
    QHash<int, int> indentList = getAllIndents(projectId);
    QList<int> sortedIdList    = getAllIds(projectId);


    // determine children

    int  parentIndent = indentList.value(treeItemId);
    bool parentPassed = false;

    for (int id : qAsConst(sortedIdList)) {
        if (id == treeItemId) {
            parentPassed = true;
            continue;
        }

        if (parentPassed) {
            int idIndent = indentList.value(id);

            if (idIndent == parentIndent + 1) {
                bool isTrashed = this->getTrashed(projectId, id);

                if (trashedAreIncluded && isTrashed) {
                    childrenList.append(id);
                }

                if (notTrashedAreIncluded && !isTrashed) {
                    childrenList.append(id);
                }
            }

            if (idIndent <= parentIndent) {
                break;
            }
        }
    }

    return childrenList;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getAllAncestors(int projectId, int treeItemId) const
{
    QList<int> ancestorsList;

    // get indents
    QHash<int, int> indentList = getAllIndents(projectId);
    QList<int> sortedIdList    = getAllIds(projectId);


    // determine ancestors

    int indent = indentList.value(treeItemId);


    for (int i = sortedIdList.indexOf(treeItemId); i >= 0; i--) {
        int id = sortedIdList.at(i);

        //        if (id == treeItemId) {
        //            continue;
        //        }

        int idIndent = indentList.value(id);

        if (idIndent == indent - 1) {
            if (indent == -1) {
                break;
            }

            ancestorsList.append(id);

            indent = idIndent;
        }
    }

    return ancestorsList;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getAllSiblings(int projectId, int treeItemId, bool treeItemIncluded)
{
    QList<int> siblingsList;

    // get indents
    QHash<int, int> indentList = getAllIndents(projectId);
    QList<int> sortedIdList    = getAllIds(projectId);
    int treeItemSortedIdIndex  = sortedIdList.indexOf(treeItemId);


    // determine siblings

    int indent = indentList.value(treeItemId);

    // min sibling index
    int minSiblingIndex = treeItemSortedIdIndex;

    for (int i = treeItemSortedIdIndex; i >= 0; i--) {
        int id = sortedIdList.at(i);

        //        if (id == treeItemId) {
        //            continue;
        //        }

        int idIndent = indentList.value(id);

        if ((idIndent == indent - 1) || (indent == -1)) {
            break;
        }
        minSiblingIndex = i;
    }

    // min sibling index
    int maxSiblingIndex = treeItemSortedIdIndex;

    for (int i = treeItemSortedIdIndex; i < sortedIdList.count(); i++) {
        int id = sortedIdList.at(i);

        //        if (id == treeItemId) {
        //            continue;
        //        }

        int idIndent = indentList.value(id);

        if ((idIndent == indent - 1) || (indent == -1)) {
            break;
        }
        maxSiblingIndex = i;
    }

    // alone, so no siblings
    if ((minSiblingIndex == treeItemSortedIdIndex) &&
            (maxSiblingIndex == treeItemSortedIdIndex)) {
        return siblingsList;
    }

    // same level

    for (int i = minSiblingIndex; i <= maxSiblingIndex; i++) {
        int id = sortedIdList.at(i);

        //        if (id == treeItemId) {
        //            continue;
        //        }

        int idIndent = indentList.value(id);

        if (idIndent == indent) {
            siblingsList.append(id);
        }
    }

    if (!treeItemIncluded) {
        siblingsList.removeAll(treeItemId);
    }


    return siblingsList;
}

// ----------------------------------------------------------------------------------------

QDateTime SKRTreeHub::getTrashedDate(int projectId, int treeItemId) const
{
    return get(projectId, treeItemId, "dt_trashed").toDateTime();
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getTreeRelationshipSourcesFromReceiverId(int projectId, int receiverTreeItemId) const
{
    SKRResult  result;
    QList<int> list;
    QHash<int, QVariant> out;
    PLMSqlQueries queries(projectId, "tbl_tree_relationship");

    result = queries.getValueByIds("l_tree_source_code", out, "l_tree_receiver_code", receiverTreeItemId);

    IFOK(result) {
        list = HashIntQVariantConverter::convertToIntInt(out).values();
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return list;
}

// ----------------------------------------------------------------------------------------

QList<int>SKRTreeHub::getTreeRelationshipReceiversFromSourceId(int projectId, int sourceTreeItemId) const
{
    SKRResult  result;
    QList<int> list;
    QHash<int, QVariant> out;
    PLMSqlQueries queries(projectId, "tbl_tree_relationship");

    result = queries.getValueByIds("l_tree_receiver_code", out, "l_tree_source_code", sourceTreeItemId);

    IFOK(result) {
        list = HashIntQVariantConverter::convertToIntInt(out).values();
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return list;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTreeRelationship(int projectId, int sourceTreeItemId, int receiverTreeItemId)
{
    SKRResult result(this);

    QHash<int, int> hash;
    QHash<int, QVariant> out;

    QHash<QString, QVariant> where;

    where.insert("l_tree_receiver_code", receiverTreeItemId);
    where.insert("l_tree_source_code",   sourceTreeItemId);

    PLMSqlQueries queries(projectId, "tbl_tree_relationship");


    // verify if the relationship doesn't yet exist
    result = queries.getValueByIdsWhere("l_tree_relationship_id", out, where);

    int key = -2;

    IFOK(result) {
        hash = HashIntQVariantConverter::convertToIntInt(out);

        QHash<int, int>::const_iterator i = hash.constBegin();

        while (i != hash.constEnd()) {
            key = i.key();
            ++i;
        }

        if (hash.isEmpty() || (key == -2) || (key == 0)) {
            // no relationship exists, creating one

            int newId = -2;
            QHash<QString, QVariant> values;
            values.insert("l_tree_receiver_code", receiverTreeItemId);
            values.insert("l_tree_source_code",   sourceTreeItemId);
            result = queries.add(values, newId);

            IFOK(result) {
                emit treeRelationshipAdded(projectId, sourceTreeItemId, receiverTreeItemId);
                emit projectModified(projectId);
            }
        }
    }
    return result;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::removeTreeRelationship(int projectId, int sourceTreeItemId, int receiverTreeItemId)
{
    SKRResult result(this);

    QHash<int, int> hash;
    QHash<int, QVariant> out;

    QHash<QString, QVariant> where;

    where.insert("l_tree_receiver_code", receiverTreeItemId);

    PLMSqlQueries queries(projectId, "tbl_tree_relationship");

    result = queries.getValueByIdsWhere("l_tree_source_code", out, where);

    int key = -2;

    IFOK(result) {
        hash = HashIntQVariantConverter::convertToIntInt(out);

        QHash<int, int>::const_iterator i = hash.constBegin();

        while (i != hash.constEnd()) {
            key = i.key();
            ++i;
        }

        if (hash.isEmpty() || (key == -2) || (key == 0)) {
            result = SKRResult(SKRResult::Critical, this, "no_tree_relationship_to_remove");
        }
    }

    IFOK(result) {
        result = queries.remove(key);
    }
    IFOK(result) {
        emit treeRelationshipRemoved(projectId, sourceTreeItemId, receiverTreeItemId);
        emit projectModified(projectId);
    }
    IFKO(result) {
        emit errorSent(result);
    }

    return result;
}

// ----------------------------------------------------------------------------------------
SKRResult SKRTreeHub::addQuickNote(int projectId, int receiverTreeItemId, const QString& type, const QString& noteName)
{
    SKRResult result(this);

    QList<int> noteFolders = this->getIdsWithInternalTitle(projectId, "note_folder");

    int noteFolderId = -2;

    if (noteFolders.isEmpty()) {
        noteFolderId = 0; // project item id
    }
    else {
        noteFolderId = noteFolders.takeFirst();
    }

    result = this->addChildTreeItem(projectId, noteFolderId, type);

    int noteId = -2;
    IFOK(result) {
        noteId = result.getData("treeItemId", -2).toInt();

        if (noteId == -2) {
            result = SKRResult(SKRResult::Critical, this, "add_quick_note_error");
        }
    }
    IFOK(result) {
        result = this->setTitle(projectId, noteId, noteName);
    }
    IFOK(result) {
        result = this->setTreeRelationship(projectId, noteId, receiverTreeItemId);
    }


    return result;
}

// ----------------------------------------------------------------------------------------

int SKRTreeHub::getPreviousTreeItemIdOfTheSameType(int projectId, int treeItemId) const
{
    SKRResult result(this);
    int previousTreeItemId = -1;

    QList<int> allIds = this->getAllIds(projectId);

    int thisItemIndex    = allIds.indexOf(treeItemId);
    QString thisItemType = this->getType(projectId, treeItemId);

    if (thisItemIndex == -1) {
        result = SKRResult(SKRResult::Critical, this, "no_index_found");
    }

    if (thisItemIndex <= 1) {
        return -1;
    }

    IFOK(result) {
        for (int i = thisItemIndex - 1; i >= 0; i--) {
            int potentiallyPreviousItemId = allIds.at(i);

            if (!this->getTrashed(projectId, potentiallyPreviousItemId)) {
                QString previousItemType = this->getType(projectId, potentiallyPreviousItemId);

                if (previousItemType == thisItemType) {
                    previousTreeItemId = potentiallyPreviousItemId;
                    break;
                }
            }
        }
    }
    IFKO(result) {
        emit errorSent(result);
    }

    return previousTreeItemId;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::duplicateTreeItem(int projectId, int treeItemId, bool duplicateChildren, bool renumber)
{
    SKRResult result(this);
    QList<int> resultTreeItemIdList;

    QHash<QString, QVariant> values;

    int validSortOrder = getValidSortOrderAfterTree(projectId, treeItemId);

    values.insert("t_title",             getTitle(projectId, treeItemId));
    values.insert("l_indent",            getIndent(projectId, treeItemId));
    values.insert("l_sort_order",        validSortOrder);
    values.insert("t_type",              getType(projectId, treeItemId));
    values.insert("m_primary_content",   getPrimaryContent(projectId, treeItemId));
    values.insert("m_secondary_content", getSecondaryContent(projectId, treeItemId));

    result = this->addTreeItem(values, projectId, false);

    int newTreeItemId = result.getData("treeItemId", -2).toInt();
    resultTreeItemIdList << newTreeItemId;

    if(duplicateChildren){
        QList<int> childrenList = getAllChildren(projectId, treeItemId);
        QList<int> childrenNotTrashed;
        for(int childId: childrenList){
            if(!getTrashed(projectId, childId)){
                childrenNotTrashed.append(childId);
            }
        }
        childrenList = childrenNotTrashed;

        int sortOrderOffset = 1;
        for(int childId: childrenList){

            QHash<QString, QVariant> childValues;

            childValues.insert("t_title",             getTitle(projectId, childId));
            childValues.insert("l_indent",            getIndent(projectId, childId));
            childValues.insert("l_sort_order",        validSortOrder + sortOrderOffset);
            childValues.insert("t_type",              getType(projectId, childId));
            childValues.insert("m_primary_content",   getPrimaryContent(projectId, childId));
            childValues.insert("m_secondary_content", getSecondaryContent(projectId, childId));
            result = this->addTreeItem(childValues, projectId, false);

            resultTreeItemIdList << result.getData("treeItemId", -2).toInt();

            sortOrderOffset += 1;

        }
    }
    if(renumber){
        IFOKDO(result, renumberSortOrders(projectId))
    }
    IFOK(result) {
        result.addData("treeItemIdList", QVariant::fromValue<QList<int> >(resultTreeItemIdList));
    }
    IFKO(result) {
        emit errorSent(result);
    }
    return result;
}

// ----------------------------------------------------------------------------------------

void SKRTreeHub::cut(int projectId, QList<int>treeItemIds)
{
    // unset old treeItems
    m_cutCopy.hasRunOnce = true;
    int oldProjectId = m_cutCopy.projectId;

    for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
        emit cutCopyChanged(oldProjectId, treeItemId, false);
    }

    // set new treeItems
    m_cutCopy = CutCopy(CutCopy::Cut, projectId, treeItemIds);

    for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
        emit cutCopyChanged(projectId, treeItemId, true);
    }
}

// ----------------------------------------------------------------------------------------

void SKRTreeHub::copy(int projectId, QList<int>treeItemIds)
{
    // unset old treeItems
    m_cutCopy.hasRunOnce = true;
    int oldProjectId = m_cutCopy.projectId;

    for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
        emit cutCopyChanged(oldProjectId, treeItemId, false);
    }

    // set new treeItems
    m_cutCopy = CutCopy(CutCopy::Copy, projectId, treeItemIds);

    for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
        emit cutCopyChanged(projectId, treeItemId, true);
    }
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::paste(int targetProjectId, int parentTreeItemId, bool copyChildren)
{
    SKRResult  result(this);
    QList<int> treeItemIdList;
    QList<int> originalTreeItemIdList = m_cutCopy.treeItemIds;
    int sourceProjectId               = m_cutCopy.projectId;

    if (m_cutCopy.type != CutCopy::Type::None) {
        if (m_cutCopy.type == CutCopy::Type::Cut) {
            if (targetProjectId == sourceProjectId) {
                for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
                    result = this->moveTreeItemAsChildOf(sourceProjectId,
                                                         treeItemId,
                                                         targetProjectId,
                                                         parentTreeItemId,
                                                         false);
                    result = this->renumberSortOrders(targetProjectId);
                    treeItemIdList << treeItemId;
                }
            }

            // TODO: case if projects are different

            // become a Copy after first paste
            m_cutCopy.projectId   = targetProjectId;
            m_cutCopy.treeItemIds = treeItemIdList;
            m_cutCopy.type        = CutCopy::Type::Copy;
        }
        else if (m_cutCopy.type == CutCopy::Type::Copy) {
            for (int treeItemId : qAsConst(m_cutCopy.treeItemIds)) {
                if (targetProjectId == sourceProjectId) {
                    result = this->duplicateTreeItem(sourceProjectId, treeItemId, copyChildren, false);
                    QList<int> newTreeItemIdList = result.getData("treeItemIdList",
                                                                  QVariant::fromValue<QList<int> >(QList<int>())).value<QList<int> >();
                    treeItemIdList << newTreeItemIdList.first();
                    IFOKDO(result,
                           this->moveTreeItemAsChildOf(sourceProjectId, newTreeItemIdList.first(), targetProjectId,
                                                       parentTreeItemId,
                                                       false))
                            result = this->renumberSortOrders(targetProjectId);
                }

                // TODO: case if projects are different
            }
        }
    }
    IFOK(result) {
        result.addData("treeItemIdList", QVariant::fromValue<QList<int> >(treeItemIdList));

        // unset old treeItems
        m_cutCopy.hasRunOnce = true;

        for (int treeItemId : qAsConst(originalTreeItemIdList)) {
            emit cutCopyChanged(sourceProjectId, treeItemId, false);
        }
    }
    IFKO(result) {
        emit errorSent(result);
    }

    IFOK(result) {
        if (m_cutCopy.type == CutCopy::Type::Cut) {
            emit treeItemMoved(sourceProjectId, treeItemIdList, targetProjectId, parentTreeItemId);

            emit projectModified(sourceProjectId);

            if (sourceProjectId != targetProjectId) {
                emit projectModified(targetProjectId);
            }
        }
        else if (m_cutCopy.type == CutCopy::Type::Copy) {
            emit treeItemsAdded(targetProjectId, treeItemIdList);

            if (sourceProjectId == targetProjectId) {
                emit projectModified(sourceProjectId);
            }
            else {
                emit projectModified(targetProjectId);
            }
        }
    }

    return result;
}

bool SKRTreeHub::isCutCopy(int projectId, int treeItemId) const {
    if ((m_cutCopy.projectId == projectId) && !m_cutCopy.hasRunOnce) {
        return m_cutCopy.treeItemIds.contains(treeItemId);
    }

    return false;
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTrashedDateToNow(int projectId, int treeItemId)
{
    return set(projectId, treeItemId, "dt_trashed", QDateTime::currentDateTime());
}

// ----------------------------------------------------------------------------------------

SKRResult SKRTreeHub::setTrashedDateToNull(int projectId, int treeItemId)
{
    return set(projectId, treeItemId, "dt_trashed", "NULL");
}

// ----------------------------------------------------------------------------------------


void SKRTreeHub::setError(const SKRResult& result)
{
    m_error = result;
}

// ----------------------------------------------------------------------------------------
